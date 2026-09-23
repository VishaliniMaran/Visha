# R&D Services Metrics Dashboard

## Run in VS Code

Open the repository in VS Code, then run these commands in the integrated terminal:

```bash
python -m venv .venv
# Windows PowerShell
.venv\\Scripts\\Activate.ps1
# macOS/Linux
source .venv/bin/activate

python -m pip install -r requirements.txt
streamlit run dashboard.py
```

The dashboard opens in your browser and includes:

- KPI totals: 949 tickets, 8,561.5 saving hours, and 225 savings (week)
- Pie chart for tickets by category
- Bar chart for saving hours by category
- Bar chart for savings (week) by category
- Detail table
- **Export metrics as CSV** button

The exported file is named `rnd_services_metrics.csv`.
