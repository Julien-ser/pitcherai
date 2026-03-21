"""Investor targeting and scoring module"""

import json
from typing import List, Dict, Any
from ..config.config import settings
from ..database import get_db, Investor, InvestorStatus


class InvestorScorer:
    """Scores investors based on relevance to user's profile"""

    def __init__(self, user_profile: Dict[str, Any]):
        self.user_profile = user_profile
        self.db = get_db()

    def calculate_relevance(self, investor: Investor) -> float:
        """Calculate a relevance score (0-1) for an investor"""
        score = 0.0

        # Match focus areas
        if investor.focus_areas:
            try:
                focus_areas = json.loads(investor.focus_areas)
                user_focus = self.user_profile.get("focus_areas", [])
                matches = set(focus_areas) & set(user_focus)
                if user_focus:
                    score += len(matches) / len(user_focus) * 0.4
            except (json.JSONDecodeError, TypeError):
                pass

        # Recent funding (more recent = higher score)
        if investor.last_funding_date:
            days_ago = (datetime.utcnow() - investor.last_funding_date).days
            if days_ago < 30:
                score += 0.3
            elif days_ago < 90:
                score += 0.2

        # Investment stage match
        if investor.investment_stage:
            preferred_stages = self.user_profile.get("preferred_stages", [])
            if investor.investment_stage in preferred_stages:
                score += 0.2

        # Firm prestige (placeholder - would need external data)
        score += 0.1  # Base score

        return min(score, 1.0)

    def score_investors(self, investors: List[Investor]) -> List[Dict]:
        """Score and rank a list of investors"""
        scored = []
        for inv in investors:
            score = self.calculate_relevance(inv)
            scored.append({"investor": inv, "score": score})

        # Sort by score descending
        scored.sort(key=lambda x: x["score"], reverse=True)
        return scored

    def get_top_prospects(self, limit: int = 50) -> List[Dict]:
        """Get top-ranked prospects from database"""
        investors = self.db.query(Investor).filter(Investor.status == InvestorStatus.PROSPECT).all()
        return self.score_investors(investors)[:limit]


class Targeter:
    """Main targeting engine"""

    def __init__(self, user_profile: Dict[str, Any] = None):
        self.user_profile = user_profile or {
            "focus_areas": ["AI/ML", "Enterprise SaaS"],
            "preferred_stages": ["Seed", "Series A"],
            "min_investment": 1000000,
        }
        self.scorer = InvestorScorer(user_profile)

    def filter_by_criteria(self, investors: List[Investor], criteria: Dict) -> List[Investor]:
        """Filter investors based on criteria"""
        filtered = []

        for inv in investors:
            # Focus area filter
            if "focus_areas" in criteria and inv.focus_areas:
                try:
                    inv_focus = json.loads(inv.focus_areas)
                    if not any(f in criteria["focus_areas"] for f in inv_focus):
                        continue
                except json.JSONDecodeError:
                    continue

            # Stage filter
            if "investment_stages" in criteria and inv.investment_stage:
                if inv.investment_stage not in criteria["investment_stages"]:
                    continue

            # Minimum score filter
            if "min_score" in criteria:
                score = self.scorer.calculate_relevance(inv)
                if score < criteria["min_score"]:
                    continue

            filtered.append(inv)

        return filtered

    def discover_and_score(self, raw_investors: List[Dict]) -> List[Dict]:
        """Convert raw investor data to Investor objects, score, and return ranked list"""
        db = get_db()
        investors = []

        for data in raw_investors:
            # Check if investor already exists
            existing = None
            if data.get("email"):
                existing = db.query(Investor).filter_by(email=data["email"]).first()

            if existing:
                inv = existing
            else:
                inv = Investor(**data)
                db.add(inv)
                try:
                    db.commit()
                    db.refresh(inv)
                except Exception as e:
                    db.rollback()
                    print(f"Error saving investor {data.get('name')}: {e}")
                    continue

            score = self.scorer.calculate_relevance(inv)
            investors.append({"investor": inv, "score": score})

        db.close()
        investors.sort(key=lambda x: x["score"], reverse=True)
        return investors


# Convenience function
def create_targeter(user_profile: Dict = None) -> Targeter:
    """Factory function to create a Targeter instance"""
    return Targeter(user_profile)
