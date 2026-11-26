# C2G coordinated expanded review editions — 26 November 2026

The full PDFs are provided in the download package. Each starts with the revised synthesis and new research sections, followed by the complete unchanged previous edition with its original page numbering and all illustrations. This deliberate approach prevents loss or silent alteration of the scientific record. These are expanded review editions, not fully re-typeset journal manuscripts. In the final journal revision, integrate the new sections into the main body and update the abstract, conclusion, references and numbering throughout.

| Paper | Baseline | Review edition | Pages | New contribution |
|---|---|---|---:|---|
| Architectural Economy | v9 | v10 | 28 | Two parallel-workload CPU pilots; protective dependency topology and H1-D |
| Functional Equivalence Mapping | v1.1 | v1.2 | 21 | Prospective H3-D regulatory dependency-diversity test; no new genomic results |
| The Augmented Investigator | v0.4 | v0.5 | 19 | Return-direction case episode and verification-dependency gate |

All three revisions preserve the reciprocal PDP-8 → biology → modern computing → biology/verification research program. The models are not actual H100 hardware results. Independent reproduction and specialist review remain pending. No new data were analyzed for this editorial revision. All prior baselines remain immutable. See revisions.md for editable revision text and RELEASE_MANIFEST.json for file hashes.

## Exact recovery from GitHub

The archive `exact_deltas.zip` contains the byte suffixes appended to the original three PDFs. `assemble_release.py` verifies the SHA-256 of each baseline and delta, concatenates the bytes, verifies the resulting PDF SHA-256, and refuses to replace a nonidentical file. No PDF tool or Python package is required. Run it from the release folder with `--repo` pointing to an up-to-date clone of the C2G repository. The full original files must be present at the manifest paths.

```powershell
python .\assemble_release.py --repo C:\path\to\circuits-to-genomes
```

To commit the reconstructed full PDFs and add links and checksums in the repository, use a clean, authenticated clone on main:

```powershell
python .\assemble_release.py --repo C:\path\to\circuits-to-genomes --publish
```

The three standalone review PDFs were published to the master repository on 26 November 2026 by a successful GitHub Actions run (45875375201); their SHA-256 values match the release manifest. The reconstruction archive remains preserved for independent recovery. The manifest is the authoritative exact-file verification record. Source of new findings: research/h100-lab/v0.1 and research/hopper-pilot/v0.2. Keep those versions unchanged.
