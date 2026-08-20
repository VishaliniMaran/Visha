# Services Dashboard

Files in this package:
- `dashboard.py` — Streamlit app to view the dashboard.
- `generate_pngs.py` — Headless script to produce PNG charts in the same folder.
- `requirements.txt` — Python dependencies.

Quick start (PowerShell):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Run Streamlit dashboard
streamlit run dashboard.py

# Or generate PNGs directly
python generate_pngs.py
```

Generated PNG paths after running `generate_pngs.py`:
- `saving_hours.png`
- `tickets.png`
- `weekly_savings.png`

