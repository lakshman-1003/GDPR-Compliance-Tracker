
"""
ISO27001/GDPR Compliance Tracker
Author: Lakshman S (auto-generated scaffold)
Usage:
  python src/main.py
Outputs:
  - reports/compliance_report.xlsx
  - reports/risk_register.csv
  - reports/risk_heatmap.png
  - reports/summary.md
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import datetime

BASE = Path(__file__).resolve().parents[1]
DATA = BASE / "data"
REPORTS = BASE / "reports"
REPORTS.mkdir(exist_ok=True, parents=True)

# Load data
controls = pd.read_csv(DATA / "controls.csv")
assets = pd.read_csv(DATA / "assets.csv")
risks = pd.read_csv(DATA / "risks.csv")
maps = pd.read_csv(DATA / "mappings.csv")

# Risk scoring
risks["risk_score"] = risks["likelihood"] * risks["impact"]

# Risk level buckets
def bucket(score):
    if score >= 20: return "Critical"
    if score >= 12: return "High"
    if score >= 8: return "Medium"
    return "Low"

risks["risk_level"] = risks["risk_score"].apply(bucket)

# Control coverage metrics
control_coverage = (
    risks.assign(control_id=risks["existing_controls"].str.split(";"))
         .explode("control_id")
         .groupby("control_id")
         .size()
         .reset_index(name="linked_risks")
)

controls_merged = controls.merge(control_coverage, on="control_id", how="left").fillna({"linked_risks":0})
controls_merged["compliance_status"] = np.where(controls_merged["status"].eq("Implemented"), "Compliant",
                                         np.where(controls_merged["status"].eq("In Progress"), "Partial", "Gap"))

# Regulation mapping coverage
map_cov = maps.groupby(["regulation","control_id"]).size().reset_index(name="mapped_requirements")
map_cov = map_cov.merge(controls_merged[["control_id","status","compliance_status"]], on="control_id", how="left")

# Risk register with asset info
risk_register = risks.merge(assets, on="asset_id", how="left")

# Save risk register CSV
risk_register.to_csv(REPORTS / "risk_register.csv", index=False)

# Summary KPIs
kpis = {
    "date_generated": datetime.date.today().isoformat(),
    "total_controls": int(len(controls)),
    "implemented_controls": int((controls_merged["status"]=="Implemented").sum()),
    "partial_controls": int((controls_merged["status"]=="In Progress").sum()),
    "gap_controls": int((controls_merged["status"]=="Not Started").sum()),
    "total_risks": int(len(risks)),
    "high_or_critical_risks": int((risk_register["risk_level"].isin(["High","Critical"])).sum())
}

# Excel report
with pd.ExcelWriter(REPORTS / "compliance_report.xlsx", engine="openpyxl") as writer:
    controls_merged.to_excel(writer, sheet_name="Controls", index=False)
    map_cov.to_excel(writer, sheet_name="Regulation Mapping", index=False)
    risk_register.to_excel(writer, sheet_name="Risk Register", index=False)
    pd.DataFrame([kpis]).to_excel(writer, sheet_name="KPIs", index=False)

# Heatmap (likelihood vs impact count)
pivot = risks.pivot_table(index="likelihood", columns="impact", values="risk_id", aggfunc="count").fillna(0)
plt.figure()
plt.imshow(pivot.values)
plt.title("Risk Heatmap (Likelihood x Impact)")
plt.xlabel("Impact")
plt.ylabel("Likelihood")
plt.xticks(ticks=range(len(pivot.columns)), labels=pivot.columns)
plt.yticks(ticks=range(len(pivot.index)), labels=pivot.index)
for i in range(pivot.shape[0]):
    for j in range(pivot.shape[1]):
        plt.text(j, i, int(pivot.values[i,j]), ha="center", va="center")
plt.tight_layout()
plt.savefig(REPORTS / "risk_heatmap.png", dpi=200)
plt.close()

# Markdown summary
summary = f"""
# Compliance Tracker Summary

**Date:** {kpis['date_generated']}

## KPIs
- Total Controls: {kpis['total_controls']}
- Implemented Controls: {kpis['implemented_controls']}
- Partial Controls: {kpis['partial_controls']}
- Gap Controls: {kpis['gap_controls']}
- Total Risks: {kpis['total_risks']}
- High/Critical Risks: {kpis['high_or_critical_risks']}

## Notes
- Update control statuses and add evidence links to improve compliance.
- Prioritize treatment plans for High and Critical risks.
- Map additional GDPR requirements as needed.
"""
with open(REPORTS / "summary.md","w") as f:
    f.write(summary.strip())
print("Reports generated in:", REPORTS)
