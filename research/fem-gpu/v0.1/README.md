# FEM-GPU v0.1 — START HERE
2026-11-26 | Exploratory research | Python | Zero additional expenditure

## Objective
Can different enhancer sequences preserve measured regulatory activity, and can predictive models help explain how? First validate prediction, then investigate mechanisms. Model predictions are not empirical equivalence, and reporter equivalence is not endogenous gene replacement.

## First session (free, CPU only)
1. Download the C2G repository using GitHub Code > Download ZIP and extract it.
2. Install Python 3.11 or 3.12 if necessary, from python.org.
3. Open PowerShell in the repository folder. Type:
   cd research/fem-gpu/v0.1
4. Type:
   py -m pip install numpy
5. Type:
   py pilot.py --demo --out demo-results
6. Open demo-results/summary.json in Notepad. This is a synthetic practice dataset, not biological evidence. On Linux replace py with python3. If an error occurs, stop and save the entire error. Use a new output directory on each run.

## Second session (real data)
Reuse existing Paper 2 files or obtain public processed files from https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE110758 and https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE110760 . Select the HAR design and three WTc N2 HAR DNA and RNA replicate files (not permutation, HS1-11 or N3). Put them in a local geo folder; rename design to GSE110758_HAR_design.tsv.gz, and replicates to WTc-N2-1-DNA.tsv.gz through WTc-N2-3-DNA.tsv.gz and WTc-N2-1-RNA.tsv.gz through WTc-N2-3-RNA.tsv.gz. Record original names and accessions.
Run: py pilot.py --geo geo --out real-results
Check active count against the prior 386; if different, stop and audit cohort definitions. The legacy validation helper is reused; this is not independent reproduction of TOST. No raw data redistribution.

## Interpret results
MAE is mean absolute error, smaller is better. Compare held-out prediction errors to constant activity (training mean) and zero species difference. The provisional gate requires 10% lower errors on both metrics in both all eligible and active subsets and matching prior active count. This is an engineering screen, not a statistical significance test. Do not tune to pass. Save failures as well as successes.

## Free CUDA option
Google Colab https://colab.research.google.com/ or Kaggle https://www.kaggle.com/code . Create a notebook, run:
    !git clone https://github.com/RandoSY/circuits-to-genomes.git
    %cd circuits-to-genomes/research/fem-gpu/v0.1
    !python pilot.py --demo --out demo-cpu
For optional CUDA choose Runtime > Change runtime type > GPU, if offered, then:
    !python pilot.py --demo --out demo-cuda --device cuda
PyTorch linear algebra is used, not a native CUDA kernel. Free quotas vary; no H100 guaranteed or needed. Save outputs before ending the session.

## Scientific protocol
Fixed ridge baseline: 1–3-mer frequencies, alpha=1, standardize on training data, deterministic five HAR-group folds; both species and all cuts held out together. All eligible substituted 171-bp pairs included, active subset defined by inherited negative-control 75th percentile of mean log2 activity. Activity-selected subgroup is descriptive. Audit duplicate designs, trimming, counts, normalization and negative controls. Nearby or similar HARs could still cause leakage; future chromosome/similarity blocks and untouched external assay required. The baseline cannot represent positional motif grammar.

After prediction validation, preregister a small one-hot CNN and evaluate on untouched groups. Only then use Tangermeme (https://github.com/jmschrei/tangermeme) on ten held-out pairs selected without examining explanations. Start with naturally observed alleles and existing measured permutation genotypes; test matched mutation-count/composition controls, compare observed and predicted effects. SEAM (https://github.com/evanseitz/seam-nn) can then explore attribution patterns and alternative mechanisms; these are model explanations, not proof of binding. CODA (https://doi.org/10.1038/s41586-024-08070-z) is related prior art, not proof of endogenous replacement. Freeze original FEM equivalence margin and replicate/moderation procedure before verification. Use measured activity, replicate-aware TOST and uncertainty, multiple-testing strategy and sensitivity analyses. Failure to establish equivalence is not proof of non-equivalence. Endogenous gene output needs separate experiments. All these mechanistic stages remain prospective.

## Three papers
Paper 1: related work on alternative implementations and coordination; H100 enables compute, not evidence of biology.
Paper 2: prospective prediction and mechanistic validation supplement, retain existing mixed/null findings.
Paper 3: document human-directed resource discovery, AI-assisted implementation, zero-budget decision, failures, independent review and epistemic responsibility. No private traces without approval.
No manuscript PDFs altered. Independent regulatory genomics and biostatistics review required. CAP: preserve input hashes, versions, held-out predictions, failures and conclusions. No biological result claimed yet.
