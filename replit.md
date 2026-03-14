# Yetimall Monitor Dashboard

## Overview
A Streamlit-based e-commerce competition monitoring dashboard that tracks purchase activity for a specific product on yetimall.store. It displays cumulative sales rankings, buyer leaderboards, regional distribution, and bot detection.

## Architecture
- **Language**: Python 3.12
- **Framework**: Streamlit
- **Database**: SQLite (local: `monitor.db`) with optional Supabase cloud fallback

## Key Files
- `app.py` — Main Streamlit dashboard (primary entry point)
- `config.py` — Platform/activity configuration (goods ID, deadlines, URLs)
- `processor.py` — JSON parsing and SQLite DB write logic
- `cloud_db.py` — Supabase REST API adapter (reads/writes when env vars are set)
- `main.py` — Alternative dashboard entry (references some unimplemented functions)
- `requirements.txt` — Python dependencies

## Configuration
- `GOODS_ID` in `config.py` — target product ID (default: 29860)
- `MY_USER_ID` in `app.py` — set to track your own position
- `.streamlit/config.toml` — Streamlit server config (port 5000, host 0.0.0.0)

## Optional Cloud Sync (Supabase)
Set these environment variables to enable cloud data sync:
- `SUPABASE_URL` — your Supabase project URL
- `SUPABASE_KEY` — your Supabase anon key

Without these, the app falls back to local SQLite (`monitor.db`).

## Running
The app runs via the "Start application" workflow:
```
streamlit run app.py
```
Accessible at port 5000.

## Data Flow
1. `monitor.py` (Playwright-based, not in this repo) intercepts API calls from yetimall.store
2. `processor.py` parses order JSON and writes to SQLite/Supabase
3. `app.py` reads from SQLite (local) or Supabase (cloud) and displays the dashboard
