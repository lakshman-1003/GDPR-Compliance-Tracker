# ISO 27001 / GDPR Compliance Tracker

## What’s inside
- **data/**: CSVs for controls, assets, risks, mappings.
- **policies/**: Mock policies (Markdown) to simulate an audit trail.
- **src/main.py**: Generates reports (Excel, heatmap, markdown).
- **reports/**: Auto-created outputs.

## Quick start
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
python src/main.py
```

Outputs:
- `reports/compliance_report.xlsx` – Controls, Regulation Mapping, Risk Register, KPIs
- `reports/risk_register.csv`
- `reports/risk_heatmap.png`
- `reports/summary.md`


