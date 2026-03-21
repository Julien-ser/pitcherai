"""Dashboard module - Streamlit web UI"""

import streamlit as st
import pandas as pd
from datetime import datetime
from ..database import get_db, Investor, Email, Campaign, EmailStatus, InvestorStatus
from .targeter import create_targeter
from .campaign import create_campaign_orchestrator
from .drafter import create_drafter
from .email import create_email_sender

st.set_page_config(page_title="PitcherAI", layout="wide")


def render_header():
    """Render dashboard header"""
    st.title("📧 PitcherAI Dashboard")
    st.markdown("AI-Powered VC Outreach Automation")
    st.divider()


def render_stats():
    """Render key statistics"""
    db = get_db()
    try:
        total_investors = db.query(Investor).count()
        total_emails = db.query(Email).count()
        sent_emails = db.query(Email).filter_by(status="sent").count()
        replied = db.query(Email).filter_by(status="replied").count()
        active_campaigns = db.query(Campaign).filter_by(status="active").count()

        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Total Investors", total_investors)
        col2.metric("Emails Drafted", total_emails)
        col3.metric("Emails Sent", sent_emails)
        col4.metric("Replies", replied)
        col5.metric("Active Campaigns", active_campaigns)
    finally:
        db.close()


def render_investors_table():
    """Render investors table"""
    st.subheader("🎯 Top Investors")

    db = get_db()
    try:
        investors = (
            db.query(Investor)
            .filter_by(status="prospect")
            .order_by(Investor.relevance_score.desc())
            .limit(20)
            .all()
        )

        if investors:
            data = []
            for inv in investors:
                data.append(
                    {
                        "ID": inv.id,
                        "Name": inv.name,
                        "Firm": inv.firm or "",
                        "Email": inv.email or "",
                        "Score": f"{inv.relevance_score:.2f}",
                        "Stage": inv.investment_stage or "",
                        "Status": inv.status.value if inv.status else "prospect",
                    }
                )

            df = pd.DataFrame(data)
            st.dataframe(df, use_container_width=True)

            selected_id = st.selectbox(
                "Select investor to draft email", [inv.id for inv in investors]
            )
            if st.button("Draft Email"):
                draft_email(selected_id)
        else:
            st.info("No investors found. Run the collector first!")
    finally:
        db.close()


def draft_email(investor_id: int):
    """Draft an email for selected investor"""
    with st.spinner("Drafting email..."):
        drafter = create_drafter()
        email = drafter.draft_for_investor(investor_id)
        if email:
            st.success("Email drafted!")
            st.write("**Subject:**", email.subject)
            st.text_area("Body", email.body, height=300)

            if st.button("Send Email", key=f"send_{email.id}"):
                sender = create_email_sender()
                if sender.send_pending_email(email.id):
                    st.success("Email sent!")
                else:
                    st.error("Failed to send email")
        else:
            st.error("Failed to draft email")


def render_campaigns():
    """Render campaigns section"""
    st.subheader("🚀 Campaigns")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Create New Campaign**")
        campaign_name = st.text_input("Campaign Name")
        if st.button("Create Campaign"):
            orchestrator = create_campaign_orchestrator()
            campaign = orchestrator.create_campaign(campaign_name)
            st.success(f"Campaign '{campaign_name}' created!")

    with col2:
        st.write("**Active Campaigns**")
        db = get_db()
        try:
            campaigns = db.query(Campaign).filter_by(status="active").all()
            for camp in campaigns:
                st.write(f"- {camp.name} (ID: {camp.id})")
        finally:
            db.close()


def render_quick_actions():
    """Render quick action buttons"""
    st.subheader("⚡ Quick Actions")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Run Collector", type="secondary"):
            st.info("Collector not yet implemented")

    with col2:
        if st.button("Generate All Drafts", type="secondary"):
            st.info("Batch drafting - configure campaign first")

    with col3:
        if st.button("Send Pending", type="secondary"):
            st.info("Auto-send - configure Gmail API first")


def main():
    """Main dashboard entry point"""
    render_header()
    render_stats()
    render_quick_actions()
    render_investors_table()
    render_campaigns()


if __name__ == "__main__":
    main()
