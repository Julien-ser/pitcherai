"""Base collector interface."""

from abc import ABC, abstractmethod
from typing import List, Dict, Any


class BaseCollector(ABC):
    """Base class for all data collectors."""

    @abstractmethod
    def get_recent_funding_rounds(self, days_back: int = 7) -> List[Dict[str, Any]]:
        """Get recent funding announcements."""
        pass

    @abstractmethod
    def get_investor_details(self, investor_id: str) -> Dict[str, Any]:
        """Get detailed information about an investor."""
        pass

    @abstractmethod
    def search_investors(self, criteria: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Search for investors matching criteria."""
        pass
