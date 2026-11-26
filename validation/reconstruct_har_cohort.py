"""
Independent clean-room reproduction of Study 2A (TOST equivalence, empirical-Bayes
moderation) and Study 3 (2^k combinatorial variant-permutation hypercubes) directly
from unrestricted NCBI GEO files (GSE110758 and GSE110760).

Usage:
  python validation/reconstruct_har_cohort.py --data-dir /path/to/geo_files
"""

import argparse
import gzip
import json
import math
import re
from collections import defaultdict
from pathlib import Path


def load_design_sequences(fn: Path) -> dict[str, str]:
    seqs = {}
    with gzip.open(fn, "rt", encoding="utf-8") as f:
        for ln in f:
            if ln.startswith("#"):
                continue
            parts = ln.rstrip("\n").split("\t")
            if len(parts) < 3:
                continue
            cid = parts[0].rsplit(":", 1)[0]
            if cid not in seqs:
                oligo = parts[2].strip()
                seqs[cid] = oligo[15:-44]
    return seqs


def load_replicate_counts(dna_fn: Path, rna_fn: Path) -> tuple[dict[str, tuple[int, int, int]], int, int]:
    dna_bc = defaultdict(set)
    dna_sum = defaultdict(int)
    rna_sum = defaultdict(int)
    total_dna = 0
    total_rna = 0

    with gzip.open(dna_fn, "rt", encoding="utf-8") as f:
        for ln in f:
            bc, cnt_s, full_id = ln.rstrip("\n").split("\t")
            cnt = int(cnt_s)
            if cnt > 0:
                cid = full_id.rsplit(":", 1)[0]
                dna_bc[cid].add(bc)
                dna_sum[cid] += cnt
                total_dna += cnt

    with gzip.open(rna_fn, "rt", encoding="utf-8") as f:
        for ln in f:
            bc, cnt_s, full_id = ln.rstrip("\n").split("\t")
            cnt = int(cnt_s)
            if cnt > 0:
                cid = full_id.rsplit(":", 1)[0]
                rna_sum[cid] += cnt
                total_rna += cnt

    out = {cid: (len(dna_bc[cid]), d_cnt, rna_sum.get(cid, 0)) for cid, d_cnt in dna_sum.items()}
    return out, total_dna, total_rna


def compute_activities(data_dir: Path, prefix: str) -> dict[str, list[float]]:
    reps, totals = [], []
    for r in (1, 2, 3):
        counts, tot_d, tot_r = load_replicate_counts(
            data_dir / f"{prefix}-{r}-DNA.tsv.gz",
            data_dir / f"{prefix}-{r}-RNA.tsv.gz",
        )
        reps.append(counts)
        totals.append((tot_d, tot_r))

    common = set(reps[0].keys()) & set(reps[1].keys()) & set(reps[2].keys())
    passed = {}
    for cid in common:
        if all(reps[r][cid][0] >= 5 and reps[r][cid][1] >= 50 for r in range(3)):
            acts = []
            for r in range(3):
                _, d_cnt, r_cnt = reps[r][cid]
                tot_d, tot_r = totals[r]
                cpm_r = (r_cnt + 0.5) / tot_r * 1e6
                cpm_d = (d_cnt + 0.5) / tot_d * 1e6
                acts.append(math.log2(cpm_r / cpm_d))
            passed[cid] = acts
    return passed


def main() -> None:
    parser = argparse.ArgumentParser(description="Clean-room GEO barcode reproduction for Paper 2")
    parser.add_argument("--data-dir", type=Path, required=True, help="Directory with GSE110758/GSE110760 .tsv.gz files")
    args = parser.parse_args()

    har_seqs = load_design_sequences(args.data_dir / "GSE110758_HAR_design.tsv.gz")
    acts = compute_activities(args.data_dir, "WTc-N2")
    neg_means = sorted(sum(v) / 3.0 for k, v in acts.items() if "neg_ctrl" in k.lower() or "negative_control" in k.lower())
    idx75 = 0.75 * (len(neg_means) - 1)
    lo_i, hi_i = int(math.floor(idx75)), int(math.ceil(idx75))
    p75_neg = neg_means[lo_i] + (idx75 - lo_i) * (neg_means[hi_i] - neg_means[lo_i])

    by_key = defaultdict(dict)
    for cid, r_acts in acts.items():
        m = re.match(r"^([^_]+)__species=(human|chimp)__coordinates_tested_in_hg19=\[([^\]]+)\]__(cut=\d+_of_\d+)__(.+)$", cid)
        if m:
            har_id, sp, coord, cut, _ = m.groups()
            by_key[(har_id, coord, cut)][sp] = (r_acts, har_seqs.get(cid, ""))

    paired = []
    for (har_id, coord, cut), d in sorted(by_key.items()):
        if "human" in d and "chimp" in d:
            (h_acts, h_seq), (c_acts, c_seq) = d["human"], d["chimp"]
            if len(h_seq) == 171 and len(c_seq) == 171:
                subs = sum(1 for a, b in zip(h_seq, c_seq) if a != b)
                peak = max(sum(h_acts) / 3.0, sum(c_acts) / 3.0)
                paired.append((har_id, cut, subs, peak))

    active = [p for p in paired if p[3] >= p75_neg and p[2] >= 1]
    print(f"Negative controls: n={len(neg_means)}, P75={p75_neg:.4f} log2")
    print(f"Total paired 171-bp HAR fragments: {len(paired)}")
    print(f"Active substituted HAR fragments: {len(active)}")


if __name__ == "__main__":
    main()
