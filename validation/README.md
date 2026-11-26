# Validation & Audit Artifacts (Paper 2 v1.1)

This folder records machine-readable audit outputs and clean-room verification scripts supporting the Version 1.1 revision of **Paper 2 (*Functional Equivalence Mapping in Primate Enhancer Evolution*)**. No third-party raw sequencing data are redistributed here; all primary datasets are retrieved directly from public NCBI GEO accessions (`GSE110758` and `GSE110760`).

## Contents

- `jaspar_ucsc_encode_audit_v1_1.json` — Deterministic summary of:
  1. Official human **JASPAR** (`tax_id=9606`) Position Weight Matrix (PWM) benchmark across the `n = 386` active HAR pairs in `GSE110760` (`LOCO ROC-AUC` `0.5971` baseline / `0.6014` IUPAC $\to$ **`0.6260`** JASPAR; Brier `0.2256` $\to$ `0.2206`; multivariate peak PWM disruption $\beta = -0.1312$, $p = 0.00084$; zero-parameter $|\Delta|$ $r = +0.264$, $p = 1.4 \times 10^{-7}$ and signed $\Delta$ $r = +0.199$, $p = 8.4 \times 10^{-5}$).
  2. **Ensembl** `GRCh37` $\to$ `GRCh38` coordinate mapping, **UCSC** 30-primate (`phyloP30way`) and 470-mammal (`phyloP470wayBW`) basewise conservation plus **ENCODE** ChIP-seq TF clusters (`encRegTfbsClustered`) on flagship HARs (`2xHAR.1`, `2xHAR.142`, `2xHAR.518`).
  3. **ENCODE Registry of cCREs (`SCREEN`)** coverage check (`0/12` hits within $\pm 500\text{ bp}$ across audited fetal/NPC HARs).
  4. Exact `df = 2` Student-$t$ critical-value audit (`|t| > 4.303` two-sided 95% vs. `|t| > 2.920` two-sided 90%) across the eight complete $2^k$ HAR hypercubes (`768` genotypes).
- `jaspar_24_pwms.json` — The 24 resolved human JASPAR log2-odds PWMs (`MA0143.5` `SOX2`, `MA0488.2` `JUN`, `MA1109.2` `NEUROD1`, `MA1930.2` `CTCF`, etc.).
- `reconstruct_har_cohort.py` — Independent zero-dependency Python verification script reproducing raw barcode aggregation, negative-control thresholding ($n = 120$, $P_{75} = 0.0045\text{ log}_2$), Smyth empirical-Bayes moderation, and $2^k$ hypercube epistasis directly from NCBI GEO `GSE110758` / `GSE110760` files.

## Remaining external review gate

Automated code reproduction and multi-database sensitivity auditing do not substitute for independent human peer review in biostatistics and regulatory genomics (see [../docs/VALIDATION.md](../docs/VALIDATION.md)).
