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

## How to extend (talking points for interview)
1. **Add more controls** in `data/controls.csv` and map them in `data/mappings.csv`.
2. **Integrate evidence** (links/screenshots) for implemented controls.
3. **Enhance risk model**: add treatment cost, residual risk, RTO/RPO.
4. **Automate scans**: import outputs from tools (Nmap, ZAP) and parse into `risks.csv`.
5. **Dashboards**: load the CSV/Excel into Power BI/Tableau for visual monitoring.
6. **Audit Simulation**: Update policy markdowns, create an audit checklist, and record findings.
7. **GDPR focus**: Add data subject rights, DPIA records, and processing activities.

## Resume bullet (ATS-optimized)
- Built a **Compliance Tracker System** for **ISO 27001 and GDPR**, with risk scoring, control coverage mapping, audit-ready reports (Excel/heatmap/KPIs), and mock policy evidence to strengthen governance and risk management.
