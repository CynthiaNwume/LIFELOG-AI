# LifeLog AI

LifeLog AI is a full-stack, AI-powered personal analytics application that helps users track daily wellness metrics and generate weekly insights based on behavioral trends.

---

## Overview

LifeLog AI allows users to log daily data such as mood, sleep, activity, and notes. The system analyzes recent patterns and uses an AI model to generate concise, human-readable weekly insights.

The goal is to demonstrate how AI can be integrated responsibly into a real-world data pipeline — not as a gimmick, but as a meaningful layer on top of structured data.

---

## Why This Exists

Many wellness apps collect data but fail to provide actionable insights.

LifeLog AI focuses on:
- clean data modeling
- transparent analytics
- calm, non-judgmental AI summaries
- clear separation between frontend, backend, database, and AI layers

---

## Features

- Daily wellness logging (mood, sleep, steps, notes)
- REST API built with FastAPI
- PostgreSQL-backed data storage
- Streamlit web dashboard
- Trend visualization and summary metrics
- AI-generated weekly insights based on recent data

---

## Tech Stack

- **Backend:** Python, FastAPI, SQLAlchemy
- **Frontend:** Streamlit
- **Database:** PostgreSQL
- **Analytics:** Pandas, Plotly
- **AI:** OpenAI API
- **Environment:** Python virtual environment

---

## Architecture

```text
Streamlit Frontend
        ↓
FastAPI Backend
        ↓
PostgreSQL Database
        ↓
AI Insight Generator (LLM)
