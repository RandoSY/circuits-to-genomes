"""Reproduce descriptive contrasts from Seaver & Imlay 2001 (Table 3, Table 2 and text).
Run: python analyze_system.py; no dependencies. No statistical inference.
"""
import csv,json
from pathlib import Path
p=Path(__file__).parent
with (p/"ecoli_2001.csv").open(newline="") as f:
    r={x["genotype"]:x for x in csv.DictReader(f)}
z=lambda g: float(r[g]["zone_from_disk_edge_cm"])
wt=z("wild_type")
out={
    "zone_single_KatG_minus_wt_cm":round(z("katG")-wt,2),
    "zone_single_Ahp_minus_wt_cm":round(z("ahpCF")-wt,2),
    "zone_double_KatG_Ahp_minus_wt_cm":round(z("ahpCF_katG")-wt,2),
    "zone_additive_scale_interaction_cm":round(z("ahpCF_katG")-z("katG")-z("ahpCF")+wt,2),
    "extracellular_peroxide_detection_limit_uM_approx":0.04,
    "triple_to_detection_limit_ratio":float(r["ahpCF_katG_katE"]["extracellular_peroxide_uM"])/0.04,
    "reporter_Ahp_minus_to_WT_aerobic_ratio":0.35/0.03,
    "reporter_exogenous_catalase_reduction_fraction":(0.35-0.18)/0.35,
    "warning":"Descriptive only. Disk diffusion distance is not linear in activity or fitness; censored measurements are not zeros."
}
print(json.dumps(out,indent=2))
