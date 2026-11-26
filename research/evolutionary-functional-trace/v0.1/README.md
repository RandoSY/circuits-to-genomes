# Evolutionary Functional Trace (EFT) v0.1 — 26 November 2026

## Goal
Trace detectable homologous DNA and reconstructed ancestral sequence through primate and mammalian branches; distinguish sequence ancestry from functional and architectural continuity. No claim of tracing human enhancers to LUCA. Ancient cellular machinery is a separate study.

## Completed local selection
Input: operator's FEM-GPU v0.1 real cohort.csv (SHA256 e178b8a5e5a5ec02e478efbdcbe9e9059ae5b2631fe6c6bbc14f2c73a2de6c00). From 813 eligible pairs, 386 active, screen for active single 171-bp constructs, no restriction-site modification tags, ACGT, and 171-bp coordinate span. 200 distinct HARs eligible. Deterministically rank SHA256 of EFT-v0.1|HAR_ID; first ten below. No selection on direction or size of activity difference. These are a convenience pilot, not a population sample. Coordinates are treated as candidate hg19 BED intervals pending exact sequence verification.

| HAR | hg19 candidate interval | Hamming mismatches | Human minus chimp mean log2 activity |
|---|---|---:|---:|
| 2xHAR.60 | chr4:28979920-28980091 | 8 | -0.136847 |
| 2xHAR.463 | chr9:14292841-14293012 | 4 | 0.107451 |
| 2xHAR.551 | chr16:8407942-8408113 | 7 | 0.008033 |
| 2xHAR.297 | chr9:129126304-129126475 | 5 | 0.013813 |
| 2xHAR.519 | chr4:167095643-167095814 | 5 | 0.184354 |
| 2xHAR.494 | chr3:61205944-61206115 | 5 | 0.050834 |
| 2xHAR.290 | chr2:156619180-156619351 | 6 | -0.154324 |
| 2xHAR.556 | chr3:67788065-67788236 | 4 | 0.298248 |
| 2xHAR.119 | chr2:142547681-142547852 | 31 | -0.065416 |
| 2xHAR.13 | chr20:36479515-36479686 | 8 | 0.074838 |

Hamming mismatch count is not a confirmed substitution count. Audit indels and offset in 2xHAR.119. Small observed delta is not TOST equivalence.

## Windows, free, no packages
From this directory:
```powershell
py trace.py --cohort "$env:USERPROFILE\Desktop\circuits-to-genomes\research\fem-gpu\v0.1\real-results\cohort.csv" --out trace-results --online
```
Use new output directory on retries. Send summary.json and the complete trace-results folder zipped. No raw biological data committed. Local selection executed; live network unavailable in execution environment, so online portion untested. The code requests Ensembl GRCh37-to-GRCh38 mapping and requires exact assay reference identity in either orientation. Requests EPO primate/mammal alignments, saves JSON and phyloXML, compares bases only for a full reference block. Failure to retrieve or align is not biological absence. Provider internal nodes need assignment to clades before interpretation.

## Next gates
Verify synteny and chimp reference identity, compare alignment coverage and validate node assignment, reconstruct ancestral sequences with explicit model uncertainty, scan versioned motif matrices, and test measured ancestral reporter activity when available. The failed v0.1 prediction gate blocks claims about predicted ancestral function. Endogenous functional replacement requires additional evidence. Expand to vertebrates only with defensible homology. For LUCA use ancient protein/RNA families separately.
Paper 1: prospective architectural lineage. Paper 2: prospective ancestral sequence and functional validation. Paper 3: record selection, uncertainty, network blocker and verification. No manuscript edits or new ancestry results claimed.
Sources: https://rest.ensembl.org/documentation/info/assembly_map ; https://rest.ensembl.org/documentation/info/genomic_alignment_region ; https://useast.ensembl.org/info/genome/compara/multiple_genome_alignments.html
