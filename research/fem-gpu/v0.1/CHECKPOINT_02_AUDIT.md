# Checkpoint 02A — processed-output audit, 26 November 2026

## Scope
Independent reimplementation in Python/NumPy from operator-uploaded cohort, predictions and summary, not fresh reconstruction from GEO counts. No raw biological data redistributed. CPU only; no GPU expense. The result is negative prediction, not a test of functional equivalence or H3-M itself.

SHA-256 of exact uploaded files:
- summary(1).json: b2b9017f6f99c68ac28568014b932bf9c1232f74dd86d82d1e06290732914407
- predictions(1).csv: 285bbea77a982b7a6d6c1f296cce7dfc5c835903aa7d51cbccd2982db4eb0956
- cohort(1).csv: e178b8a5e5a5ec02e478efbdcbe9e9059ae5b2631fe6c6bbc14f2c73a2de6c00

## Independent checks
813 one-to-one pair keys across cohort and predictions, 606 HAR groups, 1626 sequences all 171 bp and valid ACGT, 4878 finite replicate activity values, no missing fields. Replicate means match reported observed activities to 2.22e-16; observed/predicted deltas match to <2e-16. Active classification exactly matches 386 flags at threshold 0.004470700746986775. Five folds: 172,154,163,156,168 pairs; 122,121,121,121,121 HAR groups. No HAR ID split and no identical sequence shared across folds. SHA256 sorting of HAR IDs and round-robin assignment reproduced exactly. Related nonidentical sequences and overlapping coordinates across HAR groups were not excluded by this check.
All four MAEs in both subsets reproduced to <5e-17. Independently reconstructed all 1626 predictions using overlapping 1–3-mer frequencies, training-only feature standardization, alpha=1 ridge and training-fold intercept; max absolute prediction difference 1.188354969983152e-13. This independently reproduces the negative baseline from processed inputs, not an independent biological dataset or earlier FEM TOST.

## Additional diagnostics
Median across-sequence sample SD of three replicate log2 activities: 0.0395034 (all), 0.0357083 (active). Median paired human-minus-chimp standard error 0.0264040 (all), assuming corresponding replicates are appropriately paired; descriptive only, not a noise ceiling.
Index-wise Hamming mismatches per pair range 1–122, median 4; 29 pairs have >20 mismatches, 18 active. Hamming counts may overstate substitutions if homologous constructs are offset or contain indels. Audit actual alignments and design coordinates before interpreting divergence or positional grammar. Do not silently exclude those pairs or change the original cohort.

## Interpretation and next step
All-pair activity improvement -7.37466%, delta improvement -2.07173%; active -4.28878%, -0.67088%. Prespecified gate failed. Synthetic validation passed but cannot establish biological generalization. Failure of the k-mer representation is compatible with, but does not establish, importance of regulatory coordination; alternative explanations include model choice, noise, sample size, omitted features and context.
Next v0.2: audit sequence alignments and construct pair identity; compare composition, positional and JASPAR motif features with frozen nested group or chromosome/similarity-block evaluation. Current data are development evidence, not untouched external validation. Keep the prior gate, quantify uncertainty by HAR-cluster resampling, use independent measured data before mechanism claims. Tangermeme and SEAM remain prospective.
Paper 1: methodological motivation only. Paper 2: reproducible negative prediction and count-level agreement, not new FEM evidence. Paper 3: documented synthetic success, biological failure, independent computational audit and adherence to stopping rule. No manuscript changes. Specialist review remains necessary.
