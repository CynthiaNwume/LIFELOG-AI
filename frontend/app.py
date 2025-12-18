"""
LifeLog AI – Streamlit Frontend
Author: Cynthia Nwume

Mobile-first, calm futuristic personal analytics dashboard.
"""

import streamlit as st
import requests
import pandas as pd
import os
from datetime import datetime

# --------------------------------------------------
# Configuration
# --------------------------------------------------
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

st.set_page_config(
    page_title="LifeLog AI",
    layout="wide",
    initial_sidebar_state="collapsed"  # better on mobile
)

# --------------------------------------------------
# Global Styling (Mobile-First)
# --------------------------------------------------
st.markdown(
    """
    <style>
        body {
            background:
              radial-gradient(1200px 600px at 10% 10%, rgba(127,90,240,0.15), transparent 40%),
              radial-gradient(900px 500px at 90% 20%, rgba(44,182,125,0.12), transparent 35%),
              linear-gradient(180deg, #0b0b14, #0a0a12 60%);
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        h1, h2, h3 {
            font-weight: 600;
            letter-spacing: 0.3px;
        }

        .accent-bar {
            height: 4px;
            width: 88px;
            background: linear-gradient(270deg, #7f5af0, #2cb67d, #7f5af0);
            background-size: 400% 400%;
            animation: gradientMove 7s ease infinite;
            border-radius: 999px;
            margin-bottom: 1rem;
        }

        @keyframes gradientMove {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        .card {
            padding: 1.4rem;
            border-radius: 18px;
            background: rgba(255,255,255,0.07);
            backdrop-filter: blur(14px);
            border: 1px solid rgba(255,255,255,0.14);
            margin-bottom: 1.6rem;
        }

        .muted {
            opacity: .75;
            font-size: .95rem;
        }

        .footer {
            margin-top: 3.5rem;
            padding-top: 1.5rem;
            border-top: 1px solid rgba(255,255,255,.2);
            text-align: center;
            font-size: .85rem;
            opacity: .75;
        }

        /* Mobile-first adjustments */
        @media (max-width: 768px) {
            .block-container {
                padding-left: 1rem;
                padding-right: 1rem;
            }

            h2 { font-size: 1.35rem; }
            h3 { font-size: 1.1rem; }

            .card {
                padding: 1.25rem;
            }
        }
    </style>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# Sidebar Navigation (Mobile Friendly)
# --------------------------------------------------
st.sidebar.markdown("## LifeLog AI")
page = st.sidebar.radio("", ["Dashboard", "About"])

# ==================================================
# DASHBOARD
# ==================================================
if page == "Dashboard":

    # ----------------------------
    # Hero
    # ----------------------------
    st.markdown(
        """
        <div class="card">
            <div class="accent-bar"></div>
            <h2>LifeLog Dashboard</h2>
            <p class="muted">
                Track patterns gently. Reflect without pressure.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ----------------------------
    # Daily Log (Vertical Flow)
    # ----------------------------
    st.markdown(
        """
        <div class="card">
            <div class="accent-bar"></div>
            <h3>Daily Log</h3>
            <p class="muted">One entry per day is enough.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    with st.form("daily_log_form", clear_on_submit=True):
        log_date = st.date_input("Date", datetime.today())
        mood = st.slider("Mood (1–10)", 1, 10, 5)
        sleep_hours = st.number_input("Sleep (hours)", 0.0, 24.0, step=0.5)
        steps = st.number_input("Steps", min_value=0, step=100)
        notes = st.text_area("Notes (optional)")

        submitted = st.form_submit_button("Save Entry")

    if submitted:
        payload = {
            "log_date": str(log_date),
            "mood": mood,
            "sleep_hours": sleep_hours,
            "steps": steps,
            "notes": notes
        }
        res = requests.post(f"{BACKEND_URL}/log-day", json=payload)
        if res.status_code == 200:
            st.success("Saved")
        else:
            st.error(res.json().get("detail", "Error"))

    # ----------------------------
    # Fetch Logs
    # ----------------------------
    res = requests.get(f"{BACKEND_URL}/logs")

    if res.status_code == 200:
        df = pd.DataFrame(res.json())

        if not df.empty:
            df["log_date"] = pd.to_datetime(df["log_date"])
            df = df.sort_values("log_date")

            # ----------------------------
            # Metrics (STACKED FOR MOBILE)
            # ----------------------------
            st.markdown(
                """
                <div class="card">
                    <div class="accent-bar"></div>
                    <h3>At a Glance</h3>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.metric("Average Mood", round(df["mood"].mean(), 1))
            st.metric("Average Sleep (hrs)", round(df["sleep_hours"].mean(), 1))
            st.metric("Average Steps", int(df["steps"].mean()))

            # ----------------------------
            # AI Insight (Readable Block)
            # ----------------------------
            st.markdown(
                """
                <div class="card">
                    <div class="accent-bar"></div>
                    <h3>Weekly Insight</h3>
                </div>
                """,
                unsafe_allow_html=True
            )

            ir = requests.get(f"{BACKEND_URL}/insights/weekly")
            if ir.status_code == 200:
                st.write(ir.json().get("insight", ""))
            else:
                st.info("Insight not available yet.")

            # ----------------------------
            # Trend (Single Focus)
            # ----------------------------
            st.markdown(
                """
                <div class="card">
                    <div class="accent-bar"></div>
                    <h3>Mood Trend</h3>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.line_chart(df.set_index("log_date")["mood"])

            with st.expander("View details"):
                st.dataframe(
                    df[["log_date", "mood", "sleep_hours", "steps", "notes"]],
                    use_container_width=True
                )

        else:
            st.info("Start logging to unlock insights.")

# ==================================================
# ABOUT
# ==================================================
elif page == "About":

    st.markdown(
        """
        <div class="card">
            <div class="accent-bar"></div>
            <h2>LifeLog AI — Case Study</h2>
            <p class="muted">
                A calm, intentional approach to personal analytics and responsible AI.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # --------------------------------------------------
    # Overview
    # --------------------------------------------------
    st.markdown(
        """
        <div class="card">
            <h3>Overview</h3>
            <p>
                LifeLog AI is a personal analytics platform designed to help individuals
                understand behavioral patterns through structured data and thoughtful AI insights.
                The project explores how calm product design can transform raw daily metrics
                into meaningful reflection, without overwhelm or judgment.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # --------------------------------------------------
    # Problem
    # --------------------------------------------------
    st.markdown(
        """
        <div class="card">
            <h3>The Problem</h3>
            <p>
                Many wellness and productivity tools focus heavily on data collection
                but stop short of interpretation. Users are often presented with charts,
                scores, and trends without context, leaving them unsure what actually matters
                or how to act on the information.
            </p>
            <p>
                This commonly leads to data fatigue, guilt-driven usage, or abandonment of the tool.
                LifeLog AI was built to address the gap between data and understanding.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # --------------------------------------------------
    # Design Philosophy
    # --------------------------------------------------
    st.markdown(
        """
        <div class="card">
            <h3>Design Philosophy</h3>
            <ul>
                <li>Clarity over density</li>
                <li>Patterns over noise</li>
                <li>Reflection over optimization</li>
                <li>AI as an assistant, not an authority</li>
            </ul>
            <p>
                The interface intentionally avoids excessive gamification, alerts,
                and visual clutter. The goal is to create a space users want to return to,
                not feel pressured by.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # --------------------------------------------------
    # Architecture
    # --------------------------------------------------
    st.markdown(
        """
        <div class="card">
            <h3>Technical Architecture</h3>
            <pre>
Streamlit Frontend
        ↓
FastAPI Backend
        ↓
PostgreSQL Database
        ↓
AI Insight Layer (LLM)
            </pre>
            <p class="muted">
                Each layer has a single responsibility, ensuring clarity,
                maintainability, and scalability.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # --------------------------------------------------
    # Key Features
    # --------------------------------------------------
    st.markdown(
        """
        <div class="card">
            <h3>Key Features</h3>
            <ul>
                <li>Daily logging of mood, sleep, steps, and notes</li>
                <li>Time-based trend analysis and summary metrics</li>
                <li>Deterministic, non-AI pattern insights</li>
                <li>AI-generated weekly reflections from structured data</li>
                <li>Exportable summaries for offline reflection</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

    # --------------------------------------------------
    # Learnings
    # --------------------------------------------------
    st.markdown(
        """
        <div class="card">
            <h3>What I Learned</h3>
            <ul>
                <li>Clean data models simplify every layer above them</li>
                <li>AI is most effective when used selectively and transparently</li>
                <li>Visual hierarchy dramatically affects usability</li>
                <li>Product thinking is as important as technical correctness</li>
            </ul>
            <p>
                This project served as both a technical build and a product design exercise.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # --------------------------------------------------
    # What's Next
    # --------------------------------------------------
    st.markdown(
        """
        <div class="card">
            <h3>What’s Next</h3>
            <ul>
                <li>Mobile-native client</li>
                <li>Insight history and longitudinal comparisons</li>
                <li>User authentication</li>
                <li>Cloud deployment and observability</li>
            </ul>
            <p class="muted">
                These enhancements are intentionally deferred to preserve
                focus and clarity in the current iteration.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )


# --------------------------------------------------
# Footer
# --------------------------------------------------
st.markdown(
    """
    <div class="footer">
        Built by <strong>Cynthia Nwume</strong><br/>
        Python · FastAPI · PostgreSQL · Streamlit · OpenAI
    </div>
    """,
    unsafe_allow_html=True
)
