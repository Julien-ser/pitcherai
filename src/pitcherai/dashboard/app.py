"""Streamlit dashboard for PitcherAI."""

import streamlit as st
import pandas as pd
from datetime import datetime
from typing import Optional
import asyncio

from pitcherai.config import settings
from pitcherai.database import get_db
from pitcherai import crud
from pitcherai.models import Campaign, CampaignTarget, Investor


st.set_page_config(
    page_title="PitcherAI Dashboard",
    page_icon="🎯",
    layout="wide",
)

st.title("🎯 PitcherAI Dashboard")
st.markdown("AI-Powered Autonomous VC Outreach Agent")


# Initialize async session
def get_async_db():
    return get_db()


@st.cache_data(ttl=30)
def get_campaigns():
    """Fetch campaigns from database."""

    async def _fetch():
        async with get_async_db() as db:
            campaigns = await crud.campaign.get_multi(db, limit=100)
            return campaigns

    return asyncio.run(_fetch())


@st.cache_data(ttl=30)
def get_campaign_targets(campaign_id: str):
    """Fetch targets for a campaign."""

    async def _fetch():
        from uuid import UUID

        async with get_async_db() as db:
            targets = await crud.campaign_target.get_by_campaign(
                db, campaign_id=UUID(campaign_id)
            )
            return targets

    return asyncio.run(_fetch())


@st.cache_data(ttl=30)
def get_investor_details(investor_id: str):
    """Fetch investor details."""

    async def _fetch():
        from uuid import UUID

        async with get_async_db() as db:
            investor = await crud.investor.get(db, id=UUID(investor_id))
            return investor

    return asyncio.run(_fetch())


def main():
    # Sidebar navigation
    page = st.sidebar.radio(
        "Navigation", ["Campaigns", "Targets Review", "Analytics", "Settings"]
    )

    if page == "Campaigns":
        show_campaigns()
    elif page == "Targets Review":
        show_targets_review()
    elif page == "Analytics":
        show_analytics()
    elif page == "Settings":
        show_settings()


def show_campaigns():
    """Display list of campaigns."""
    st.header("Campaigns")

    campaigns = get_campaigns()

    if not campaigns:
        st.info("No campaigns found. Create one via the API first!")
        return

    # Convert to dataframe
    data = []
    for camp in campaigns:
        data.append(
            {
                "ID": str(camp.id),
                "Name": camp.name,
                "Status": camp.status,
                "Started": camp.started_at.strftime("%Y-%m-%d %H:%M")
                if camp.started_at
                else "N/A",
                "Completed": camp.completed_at.strftime("%Y-%m-%d %H:%M")
                if camp.completed_at
                else "N/A",
            }
        )

    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True)

    # Show details for selected campaign
    if len(campaigns) > 0:
        st.subheader("Campaign Details")
        selected_id = st.selectbox(
            "Select campaign to view details",
            options=[str(c.id) for c in campaigns],
            format_func=lambda x: next(c.name for c in campaigns if str(c.id) == x),
        )

        if selected_id:
            targets = get_campaign_targets(selected_id)
            st.write(f"**Total Targets:** {len(targets)}")

            status_counts = {}
            for t in targets:
                status_counts[t.status] = status_counts.get(t.status, 0) + 1

            st.write("**Targets by Status:**")
            for status, count in status_counts.items():
                st.write(f"- {status}: {count}")


def show_targets_review():
    """Display campaign targets for review."""
    st.header("Targets Review")

    # Get all active/pending campaigns
    campaigns = get_campaigns()
    active_campaigns = [c for c in campaigns if c.status in ("active", "draft")]

    if not active_campaigns:
        st.info("No active campaigns found.")
        return

    # Select campaign
    campaign_options = {f"{c.name} ({c.status})": str(c.id) for c in active_campaigns}
    selected = st.selectbox("Select Campaign", options=list(campaign_options.keys()))
    campaign_id = campaign_options[selected]

    # Fetch targets
    targets = get_campaign_targets(campaign_id)

    # Filter targets needing review
    pending_targets = [
        t for t in targets if t.email_subject and t.email_body and t.status == "pending"
    ]

    if not pending_targets:
        st.success("No pending targets to review!")
        return

    st.warning(f"**{len(pending_targets)}** targets await review")

    # Display each target for review
    for idx, target in enumerate(pending_targets):
        st.divider()

        # Get investor info
        investor = get_investor_details(str(target.investor_id))
        if investor:
            st.subheader(f"{investor.name} - {investor.firm_name or 'N/A'}")
            st.write(
                f"**Focus:** {', '.join(investor.focus_areas) if investor.focus_areas else 'N/A'}"
            )
            st.write(f"**Type:** {investor.investor_type}")

        col1, col2 = st.columns(2)

        with col1:
            st.write("**Email Subject**")
            subject = st.text_input(
                "Subject",
                value=target.email_subject,
                key=f"subject_{target.id}",
                label_visibility="collapsed",
            )

            st.write("**Email Body**")
            body = st.text_area(
                "Body",
                value=target.email_body,
                height=300,
                key=f"body_{target.id}",
                label_visibility="collapsed",
            )

        with col2:
            st.write("**Actions**")
            st.write(f"Status: {target.status}")
            st.write(f"Created: {target.created_at.strftime('%Y-%m-%d')}")

            # Override notes
            override = st.text_area(
                "Override Notes (optional)",
                key=f"override_{target.id}",
                placeholder="Add any manual notes or changes...",
            )

            col_approve, col_reject, col_skip = st.columns(3)

            with col_approve:
                if st.button("✅ Approve", key=f"approve_{target.id}", type="primary"):
                    # Update via API call (placeholder)
                    st.success("Approved! (TODO: Call API)")

            with col_reject:
                if st.button("❌ Reject", key=f"reject_{target.id}"):
                    st.error("Rejected! (TODO: Call API)")

            with col_skip:
                if st.button("⏭️ Skip", key=f"skip_{target.id}"):
                    st.info("Skipped! (TODO: Call API)")


def show_analytics():
    """Display campaign analytics."""
    st.header("Analytics")

    st.info("Analytics dashboard coming soon!")

    # Placeholder for charts
    campaigns = get_campaigns()
    if campaigns:
        data = []
        for camp in campaigns:
            targets = get_campaign_targets(str(camp.id))
            sent = len([t for t in targets if t.status == "sent"])
            data.append({"Campaign": camp.name, "Sent Emails": sent})

        if data:
            df = pd.DataFrame(data)
            st.bar_chart(df.set_index("Campaign"))


def show_settings():
    """Settings page."""
    st.header("Settings")

    st.write("Configure your PitcherAI settings:")

    st.checkbox("Enable email sending", value=False, disabled=True)
    st.checkbox("Auto-approve emails", value=False)
    st.slider("Emails per day limit", min_value=10, max_value=200, value=50)

    st.button("Save Settings", type="primary", disabled=True)


if __name__ == "__main__":
    main()
