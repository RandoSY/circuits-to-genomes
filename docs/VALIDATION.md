# Validation and revision protocol

## Editorial rules

Three standalone papers, three distinct research questions, three distinct scholarly contributions. Cross-reference without substituting one paper's evidence for another's. Never treat AI agreement, polished prose, or a version number as proof.

## Paper 1

- Verify PDP-8 emulator semantics and exhaustive product checks with independent code.
- Reproduce synthetic networks and fault injection; report fault weighting, timeouts and excluded sites.
- Preserve the negative H2 pilot, sensitivity results and distinction between H3 and H3-M.
- Confirm citations and document differences between v7 and v8.

## Paper 2

- Retrieve original public datasets GSE113978, GSE110760 and GSE180714; verify IDs, sample identities, normalization and biological replicate definitions.
- Independently reproduce TOST classifications using explicit equivalence margins, raw and moderated variances, and sensitivity analyses.
- Explain margin selection and biological relevance; distinguish protocol changes from prespecified decisions.
- Clarify the 2.920 versus 4.303 t critical values for two-sided 90% versus 95% intervals at two degrees of freedom; review epistasis inference and multiple comparisons.
- Audit cohort selection, clustering, predictive validation, motif proxies and assay/cell-context confounding.
- Separate reporter activity from native gene regulation; distinguish novel contribution from prior literature.

### Recorded verification log (25 November 2026 — Paper 2 v1.1)

- Clean-room primary-barcode verification on NCBI GEO `GSE110758` / `GSE110760` confirmed `839` paired 171-bp HAR inserts, `120` negative controls (`P75 = 0.0045 log2`), and all eight complete `2^k` hypercubes (`768` genotypes) (`validation/reconstruct_har_cohort.py`).
- Post-hoc multi-database audit (`validation/jaspar_ucsc_encode_audit_v1_1.json`) separated prespecified 24-IUPAC consensus results (`LOCO ROC-AUC` 0.5971 → 0.6014) from 24 official human JASPAR PWMs (`LOCO ROC-AUC` 0.6260, Brier 0.2206, peak binding disruption `β = -0.1312`, `p = 0.00084`), Ensembl `GRCh38` mapping, UCSC `phyloP30way`/`phyloP470wayBW` conservation, ENCODE ChIP-seq TFBS, and ENCODE `SCREEN` cCRE coverage (`0/12` hits within ±500 bp across audited fetal/NPC HARs).
- Study 3 (`df = 2`) epistasis reporting now explicitly contrasts strict two-sided 95% (`|t| > 4.303`, `4/8` sub-additive saturating hypercubes) against two-sided 90% (`|t| > 2.920`, `5/8` total nonadditive hypercubes, with `2xHAR.238` at `|t| = 4.18`, `p = 0.053`).
- Historical `Primate_Enhancer_FEM_v1.pdf` is preserved unaltered in `papers/02-primate-enhancer-fem/archive/`. Independent human specialist review in biostatistics and regulatory genomics remains open.

## Paper 3

- Preserve dated prompts, artifact hashes, code versions, executed results, disagreements, and corrections in an access-controlled archive.
- Document which work is human-originated, AI-originated, joint or unclear.
- Do not infer active research time or causal productivity from document timestamps.
- Treat investigator testimony as testimony, not an objective competence measure.
- Obtain independent review of trace coding, scholarly literature and first-person disclosure.

## Release procedure

1. Record version, date, source repository and commit where known.
2. Preserve previous release; never silently overwrite a versioned artifact.
3. Record substantive changes, open issues and verification evidence.
4. Check citations, permissions and privacy. Do not publish private traces or third-party data indiscriminately.
5. Calculate SHA-256 checksums for final artifacts.
6. Obtain investigator approval and appropriate specialist review before claiming validation.

A recognized competence gap creates an obligation to seek help, not a license to overstate conclusions.
