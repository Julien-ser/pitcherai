#!/usr/bin/env python3
"""Run the PitcheRai dashboard."""

import subprocess
import sys
from src.config import settings


def run_streamlit_dashboard():
    """Launch Streamlit dashboard."""
    print("Starting PitcheRai Dashboard...")
    print(
        f"Dashboard will be available at: http://{settings.dashboard_host}:{settings.dashboard_port}"
    )
    print("Press Ctrl+C to stop\n")

    try:
        # Run streamlit
        cmd = [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            "src/dashboard/streamlit_app.py",
            "--server.address",
            settings.dashboard_host,
            "--server.port",
            str(settings.dashboard_port),
            "--server.headless",
            "false" if settings.debug else "true",
        ]
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\nDashboard stopped.")
    except FileNotFoundError:
        print("Error: Streamlit not installed. Run: pip install streamlit")
        sys.exit(1)


if __name__ == "__main__":
    run_streamlit_dashboard()
