# Checkpoint 02 — 26 November 2026
Operator-reported real CPU run: py pilot.py --geo .\download\geo --out real-results
Python 3.14.0; NumPy 2.3.5; zero reported additional expenditure. Summary pasted into conversation; CSV outputs and input files not independently inspected at this checkpoint.

## CAP — Capture
Seven input SHA-256 values reported by program:
GSE110758_HAR_design.tsv.gz c0552a2fc675f043017252a8a341d6e06cd91cedefdc7b65a0186118901a0d3f
WTc-N2-1-DNA.tsv.gz 516d3a23e53b3c8fbabc22d110ee6ef62641b563aa73655d13b4da703ad4ca31
WTc-N2-1-RNA.tsv.gz 7cbb6e1de77642aadfe815d6fbc43c368381d4acbdcf889675760d458f8c62a4
WTc-N2-2-DNA.tsv.gz f0cd36ebc9d9ed0230d2f4444d99877db372fe0af106a3cf737685c20dc56647
WTc-N2-2-RNA.tsv.gz 815e284bc2c9801146edd6bbff98ffc706bd35326f8f1d8cfaaed040510fc170
WTc-N2-3-DNA.tsv.gz 9461838b7a674bf0f312b4164848184726933a3c13c92e65aed890b55e5a5068
WTc-N2-3-RNA.tsv.gz 9d6d0ccc41791bbf7aa75ce246e4034e983f4fd738794e26d1b154c47b274899

120 negative controls; active threshold 0.004470700746986775. 324 missing or ambiguous pair keys and 26 identical pairs excluded; 813 eligible pairs, 606 HAR groups, 386 active pairs. Count and rounded threshold match prior reported results, but cohort membership and earlier TOST classifications not verified.

## CAP — Analyze
| Subset | Activity MAE model / constant | Delta MAE model / zero | Activity improvement | Delta improvement |
|---|---|---|---|---|
| All 813 | 0.11513606207063133 / 0.10722833343563695 | 0.07812132654985365 / 0.0765357149011651 | -7.37466% | -2.07173% |
| Active 386 | 0.12069128698267136 / 0.11572797006870342 | 0.09570723760804892 / 0.09506943394824358 | -4.28878% | -0.67088% |

Prediction gate false on both subsets; CPU only, CUDA not tested. This is a successful execution and a negative predictive result. The fixed k-mer ridge baseline underperforms naive comparators. It neither proves nor disproves H3-M. Do not infer that positional coordination is necessary merely because this model failed. Measurement noise, sample size, representation and regularization are alternative explanations.

## CAP — Publish and next gate
Preserve immutable v0.1 and operator outputs. Request real-results/summary.json, cohort.csv and predictions.csv to audit fold assignment, replicate means, group membership and MAE. Check possible sequence duplication across HAR groups and quantify measurement noise. Design a separate prospective v0.2 comparison of composition vs positional/motif features using nested grouped evaluation and an untouched chromosome/similarity-block or external holdout. Existing v0.1 folds are now development evidence, not untouched final validation. Do not relax the original gate after observing failure. Mechanistic attribution via Tangermeme/SEAM remains blocked pending validated predictive performance. No hardware purchase or H100 access needed.

Paper 1: negative result motivates testing representations of coordination but is not evidence of architectural economy.
Paper 2: count-level reconstruction and negative predictive baseline; no new functional equivalence finding.
Paper 3: successful software execution, prior synthetic success, real-data failure and adherence to a predefined stopping rule illustrate epistemic responsibility. Independent verification and specialist review pending.
No manuscript PDFs changed.
