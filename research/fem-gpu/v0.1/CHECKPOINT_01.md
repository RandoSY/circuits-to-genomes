# Checkpoint 01 — 2026-11-26
Operator ran FEM-GPU v0.1 on Windows, Python 3.14.0, NumPy 2.3.5, CPU. Additional hardware expenditure reported: zero.
Uploaded summary and two CSVs examined in ChatGPT; raw synthetic CSVs not redistributed in this checkpoint.
- 100 synthetic pairs, 171 nucleotides each, 12 substitutions per pair, three simulated replicates per sequence.
- Five folds of 20 pairs; each HAR identifier occurs in only one fold. No missing values. All 100 active under synthetic threshold 0.
- Activity MAE 0.05147358745902775 vs baseline 0.757164007596655; improvement 93.2018%.
- Paired delta MAE 0.03966082019171779 vs zero-delta 0.3511980966361141; improvement 88.707%.
- Independently recalculated both model MAEs from predictions.csv, matched to floating-point precision; joined one-to-one with cohort.csv and checked replicate means (max difference 3.55e-15).
- Prediction gate true, CPU only. Synthetic cohort count flag is bypassed by demo mode, not a 386-pair biological reproduction.
- This is an intentionally learnable synthetic activity model, not empirical biological evidence or independent validation of the training algorithm. CUDA and real data remain untested.
Next: recover seven GEO processed files, reproduce real active cohort count, evaluate held-out prediction and preserve failures before model interpretation. No manuscript revisions or new biological claims.
