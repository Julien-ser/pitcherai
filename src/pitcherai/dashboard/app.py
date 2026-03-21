"""Streamlit dashboard for PitcherAI."""

import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# API configuration
API_BASE_URL = "http://localhost:8000"


def api_call(method: str, endpoint: str, **kwargs):
    """Make an API call to the backend."""
    try:
        response = requests.request(
            method, f"{API_BASE_URL}{endpoint}", **kwargs, timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {e}")
        return None


st.set_page_config(
    page_title="PitcherAI Dashboard",
    page_icon="🎯",
    layout="wide",
)

st.title("🎯 PitcherAI Dashboard")
st.markdown("AI-Powered Autonomous VC Outreach Agent")


def show_campaigns():
    """Display list of campaigns."""
    st.header("Campaigns")

    campaigns = api_call("GET", "/api/campaigns")

    if not campaigns or len(campaigns) == 0:
        st.info("No campaigns found. Create one via the API first!")
        return

    # Convert to dataframe
    data = []
    for camp in campaigns:
        data.append(
            {
                "ID": camp["id"],
                "Name": camp["name"],
                "Status": camp["status"],
                "Started": camp.get("started_at", "N/A")[:19]
                if camp.get("started_at")
                else "N/A",
                "Completed": camp.get("completed_at", "N/A")[:19]
                if camp.get("completed_at")
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
            options=[c["id"] for c in campaigns],
            format_func=lambda x: next(c["name"] for c in campaigns if c["id"] == x),
        )

        if selected_id:
            targets = api_call("GET", f"/api/campaigns/{selected_id}/targets")
            if targets:
                st.write(f"**Total Targets:** {len(targets['targets'])}")

                status_counts = {}
                for t in targets["targets"]:
                    status = t["status"]
                    status_counts[status] = status_counts.get(status, 0) + 1

                st.write("**Targets by Status:**")
                for status, count in status_counts.items():
                    st.write(f"- {status}: {count}")


def show_targets_review():
    """Display campaign targets for review."""
    st.header("Targets Review")

    # Get all campaigns
    campaigns = api_call("GET", "/api/campaigns")
    if not campaigns:
        st.info("No campaigns found.")
        return

    active_campaigns = [c for c in campaigns if c["status"] in ["active", "draft"]]

    if not active_campaigns:
        st.info("No active campaigns found.")
        return

    # Select campaign
    campaign_options = {
        f"{c['name']} ({c['status']})": c["id"] for c in active_campaigns
    }
    selected = st.selectbox("Select Campaign", options=list(campaign_options.keys()))
    campaign_id = campaign_options[selected]

    # Fetch targets
    targets_resp = api_call("GET", f"/api/campaigns/{campaign_id}/targets")
    if not targets_resp:
        st.error("Failed to fetch targets")
        return

    targets = targets_resp["targets"]

    # Filter targets needing review (have email content and are pending)
    pending_targets = [
        t
        for t in targets
        if t.get("email_subject") and t.get("email_body") and t["status"] == "pending"
    ]

    if not pending_targets:
        st.success("No pending targets to review!")
        return

    st.warning(f"**{len(pending_targets)}** targets await review")

    # Display each target for review
    for idx, target in enumerate(pending_targets):
        st.divider()

        # Get investor info (would need separate API call)
        investor = api_call("GET", f"/api/investors/{target['investor_id']}")
        if investor:
            st.subheader(f"{investor['name']} - {investor.get('firm_name', 'N/A')}")
            st.write(
                f"**Focus:** {', '.join(investor.get('focus_areas', [])) or 'N/A'}"
            )
            st.write(f"**Type:** {investor['investor_type']}")

        col1, col2 = st.columns(2)

        with col1:
            st.write("**Email Subject**")
            subject = st.text_input(
                "Subject",
                value=target["email_subject"],
                key=f"subject_{target['id']}",
                label_visibility="collapsed",
            )

            st.write("**Email Body**")
            body = st.text_area(
                "Body",
                value=target["email_body"],
                height=300,
                key=f"body_{target['id']}",
                label_visibility="collapsed",
            )

        with col2:
            st.write("**Actions**")
            st.write(f"Status: {target['status']}")
            st.write(f"Created: {target['created_at'][:10]}")

            # Override notes
            override = st.text_area(
                "Override Notes (optional)",
                key=f"override_{target['id']}",
                placeholder="Add any manual notes or changes...",
            )

            col_approve, col_reject, col_skip = st.columns(3)

            with col_approve:
                if st.button(
                    "✅ Approve", key=f"approve_{target['id']}", type="primary"
                ):
                    # Update via API
                    result = api_call(
                        "PUT",
                        f"/api/campaign-targets/{target['id']}",
                        json={"status": "approved"},
                    )
                    if result:
                        st.success("Approved!")
                        st.rerun()

            with col_reject:
                if st.button("❌ Reject", key=f"reject_{target['id']}"):
                    result = api_call(
                        "PUT",
                        f"/api/campaign-targets/{target['id']}",
                        json={"status": "rejected"},
                    )
                    if result:
                        st.error("Rejected!")
                        st.rerun()

            with col_skip:
                if st.button("⏭️ Skip", key=f"skip_{target['id']}"):
                    st.info("Skipped!")
                    st.rerun()


def show_analytics():
    """Display campaign analytics."""
    st.header("Analytics")

    # Overall metrics
    overall = api_call("GET", "/api/analytics/dashboard")
    if overall:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Campaigns", overall["total_campaigns"])
        with col2:
            st.metric("Total Emails Sent", overall["total_sent_emails"])
        with col3:
            st.metric("Open Rate", f"{overall['overall_open_rate']}%")
        with col4:
            st.metric("Reply Rate", f"{overall['overall_reply_rate']}%")

    # Per-campaign analytics
    st.subheader("Campaign Performance")
    campaigns = api_call("GET", "/api/campaigns")
    if campaigns:
        data = []
        for camp in campaigns:
            analytics = api_call("GET", f"/api/analytics/campaign/{camp['id']}")
            if analytics:
                data.append(
                    {
                        "Campaign": camp["name"],
                        "Status": camp["status"],
                        "Sent": analytics["sent_count"],
                        "Opens": analytics["open_count"],
                        "Replies": analytics["reply_count"],
                        "Open Rate": f"{analytics['open_rate']}%",
                        "Reply Rate": f"{analytics['reply_rate']}%",
                    }
                )

        if data:
            df = pd.DataFrame(data)
            st.dataframe(df, use_container_width=True)


def show_settings():
    """Settings page."""
    st.header("Settings")

    st.write("Configure your PitcherAI settings:")

    st.checkbox("Enable email sending", value=False, disabled=True)
    st.checkbox("Auto-approve emails", value=False)
    st.slider("Emails per day limit", min_value=10, max_value=200, value=50)

    st.button("Save Settings", type="primary", disabled=True)


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


if __name__ == "__main__":
    main()
