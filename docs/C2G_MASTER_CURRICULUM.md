# C2G Master Curriculum v1.0
**Experience before equation · Research before accumulation**
26 November 2026 | Self-paced, zero required purchase cost | Windows PC / Python 3

## START HERE
Purpose: gain enough understanding to direct and critically evaluate the three C2G papers, not to become a specialist in every discipline. Keep the PDP-8 observation central. The H100 is a complementary example of complexity management, not a compatible PDP-8 descendant. Information theory and biological intelligence are supporting or prospective inquiries, not reasons to reopen Paper 1.

**Required route: 24 sessions, 25 minutes each (10 hours of planned study).** Three sessions per week gives eight weeks; repeat any session as needed. Setup, optional reading and difficult exercises may take longer. Each session: 5 minutes experience/observation, 10 minutes selected reading or figure, 7 minutes working example, 3 minutes explain in your own words. Stop at one useful question. No exam, deadline or hardware purchase. Python exercises use standard library; existing C2G labs may require NumPy. Never treat a toy example as biological evidence.

**First week:**
- Session 1: read the PDP-8 reference card and trace one addition.
- Session 2: inspect Paper 1's documented compatible implementations and identify what changes and what persists.
- Session 3: examine the H100 architecture diagram; identify one biological question about organization, not a claimed equivalence.

**Immediate research shortcut:** if reviewing Paper 2 now, do sessions 4–6, 10–15 before extending the computational experiments. Return to the other units when useful.

## Unit 1 — Architectural evolution (Paper 1)
**Question:** What can remain constant when the implementation changes?
Required sources: [DEC 1965 PDP-8 reference card](https://homepage.cs.uiowa.edu/~dwjones/pdp8/refcard/65.html); [1966 PDP-8 User's Handbook PDF](https://bitsavers.org/pdf/dec/pdp8/handbooks/1966_PDP8_UsersHandbook.pdf); [Paper 1 v11 PDF](../papers/01-architectural-economy/Architectural_Economy_v11.pdf); [NVIDIA Hopper architecture and whitepaper](https://www.nvidia.com/en-us/data-center/technologies/hopper-architecture/); [Hopper tuning guide](https://docs.nvidia.com/cuda/hopper-tuning-guide/).
1. **Experience:** trace TAD and DCA in a tiny PDP-8 program using octal; read the reference card. Explain instruction vs implementation.
2. **Continuity:** read Paper 1 section 2 and compare PDP-8 implementations. Specify the shared contract and exceptions (timing, peripherals, extensions). Write a two-column invariant/change table.
3. **Scale:** inspect H100 architecture and tuning-guide introductory sections. Draw threads → warps → blocks → SMs; distinguish hardware parallelism from biological analogy. Optional: [NVIDIA CUDA C++ tutorials](https://github.com/NVIDIA/accelerated-computing-hub/tree/main/tutorials/cuda-cpp), [C2G Boolean-dataflow lab](../research/h100-lab/v0.1/). No H100 required.
**Exit check:** Why does compatible execution on different PDP-8 implementations motivate, but not prove, biological functional continuity?

## Unit 2 — The regulatory genome (Paper 2)
**Question:** How does nearly the same DNA give different cell states?
Required sources: [OpenStax Biology 2e, 16.1](https://openstax.org/books/biology-2e/pages/16-1-regulation-of-gene-expression) and [16.4](https://openstax.org/books/biology-2e/pages/16-4-eukaryotic-transcription-gene-regulation); [Whalen et al., 2023, full text/PDF](https://pmc.ncbi.nlm.nih.gov/articles/PMC10023452/); [Agarwal et al., 2025, full text/PDF](https://pmc.ncbi.nlm.nih.gov/articles/PMC11903340/).
4. **Experience:** sketch DNA → RNA → protein, then identify promoter, enhancer, transcription factor and chromatin. Read 16.1/16.4 selected figures.
5. **Assay:** read Agarwal Figure 1 and Whalen assay figures; calculate log2 normalized RNA/DNA activity for ratios 1, 2 and 0.5. Compare biological replicates vs barcodes. Reporter activity is not endogenous gene output.
6. **Human/chimp:** read Whalen abstract and first main figure; examine three replicates of one pair in your local real-results/cohort.csv. Explain cis sequence vs trans cell environment.
**Exit check:** What was directly measured, and what biological function was not?
Optional: [MPRAnalyze paper, 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC6717970/), a count-model alternative, not identical to our ratio calculation.

## Unit 3 — Functional continuity and evolutionary tracing (Papers 1–2)
**Question:** Does retained function require an unchanged sequence?
Required sources: [McColgan & DiFrisco, Understanding developmental system drift (2024), PDF](https://journals.biologists.com/dev/article-pdf/151/20/dev203054/3571282/dev203054.pdf) ([PMC fallback](https://pmc.ncbi.nlm.nih.gov/articles/PMC11529278/)); [Whalen 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC10023452/); [Ensembl alignment documentation](https://rest.ensembl.org/documentation/info/genomic_alignment_region).
7. **Drift:** read the developmental system drift abstract and introductory figure. Sketch two different molecular routes to the same trait. Distinguish sequence homology from functional similarity.
8. **Compensation:** use illustrative activities ancestral 100, A 60, B 70, AB 98; compute additive contrast AB−A−B+ancestral = 68 on this chosen scale. Explain why nonadditivity alone does not establish biochemical mechanism.
9. **Ancestry:** read the [EFT v0.1 protocol](../research/evolutionary-functional-trace/v0.1/README.md). Inspect the selected ten HARs. Run locally only when ready; live alignment retrieval and ancestral activity remain unverified. Check reference identity, alignment coverage, species/clade assignment. No alignment is not proof of absence.
**Exit check:** Why can ancestral sequence reconstruction not by itself establish ancestral enhancer function?
Optional: [MIT comparative genomics lecture archive](https://compbio.mit.edu/lectures.html).

## Unit 4 — Statistics that serve the question (Paper 2)
**Question:** When is an observed similarity sufficient evidence of equivalence?
Required sources: [Lakens, free equivalence chapter](https://lakens.github.io/statistical_inferences/09-equivalencetest.html); [Lakens 2017, full text/PDF](https://pmc.ncbi.nlm.nih.gov/articles/PMC5502906/); [Irizarry & Love, hierarchical models](https://genomicsclass.github.io/book/pages/hierarchical_models.html); [Paper 2 v1.2](../papers/02-primate-enhancer-fem/Primate_Enhancer_FEM_v1.2.pdf).
10. **Uncertainty:** three synthetic paired differences -0.04, 0.00, +0.04. Compute mean, sample SD and SE. Repeat with -0.4, 0, +0.4. Explain why equal means need not imply equal certainty.
11. **TOST:** use the 90% t interval (df=2, critical value 2.920) and margin ±0.15 on both examples. Distinguish equivalent, inconclusive and evidence of a difference; tolerance chosen for teaching, not biologically justified.
12. **Borrowing strength:** read the hierarchical-model baseball example. Compare Paper 2 reported 244/386 moderated and 168/386 unmoderated at the same margin; note primary margin selected after control inspection. Explain sensitivity and why a prior does not manufacture biological replicates.
**Exit check:** Explain why a nonsignificant difference is not equivalence. Ask a specialist to evaluate the margin and moderation before consequential claims.
Optional: prior detailed [Paper 2 foundations curriculum](PAPER2_FOUNDATIONS_CURRICULUM.md), modules 3–4.

## Unit 5 — Computational genomics and validation (Paper 2)
**Question:** What does a sequence model predict, and can we trust it?
Required sources: [Whalen et al., 2022, ML pitfalls PDF](https://escholarship.org/content/qt6f5210xq/qt6f5210xq_noSplash_a2d4f168c601186bcfc04cbf01746184.pdf) ([repository landing](https://escholarship.org/uc/item/6f5210xq)); [MIT computational biology lectures](https://compbio.mit.edu/lectures.html); [JASPAR documentation](https://jaspar.elixir.no/docs/); [FEM-GPU pilot](../research/fem-gpu/v0.1/README.md).
13. **Representation:** count 1–3-mers of two short DNA sequences; then compare positions of a motif. Different order can preserve composition. PWM log odds encode preference relative to a background, not direct measured binding or energy.
14. **Prediction:** open your real FEM-GPU summary.json. Compare activity and delta MAE to their baselines. The real v0.1 gate failed; synthetic success is not validation. Read ML pitfalls sections on dependent examples and train/test leakage.
15. **Better test:** sketch grouped train/test partition by HAR; keep both species together. Define baseline and frozen criterion, then discuss independent cohort or similarity-aware holdout. Do not repeatedly tune on the same test set. Read Agarwal abstract/figures only after understanding the baseline.
**Exit check:** Why must an improved prediction precede model-based mechanistic interpretation?
Optional advanced: [Gosai et al., 2024, machine-guided design](https://www.nature.com/articles/s41586-024-08070-z) (publisher access may vary); [Whalen executable ML pitfalls notebooks](https://github.com/shwhalen/ml-pitfalls).

## Unit 6 — Information theory (supporting inquiry, not a Paper 1 rewrite)
**Question:** What is the difference between storage capacity, uncertainty and a generative description?
Required sources: [MIT 6.441 lecture notes with chapter PDFs](https://ocw.mit.edu/courses/6-441-information-theory-spring-2016/pages/lecture-notes/), chapter 1 selected definitions only; [Shuvaev et al., 2024, Encoding innate ability through a genomic bottleneck PDF](https://zadorlab.cshl.edu/wp-content/uploads/sites/59/2024/09/shuvaev-et-al-2024-Encoding-innate-ability-through-a-genomic-bottleneck-.pdf) ([PMC fallback](https://pmc.ncbi.nlm.nih.gov/articles/PMC11420173/)).
16. **Bucket:** calculate 2 bits/base × 3 billion bases / 8 = 750 million bytes. Four-symbol capacity is a maximum raw encoding size, not functional information. Compare 100 equally likely arbitrary synapse bits with 100 repeated bits.
17. **Entropy:** use exercise 16 and compute H=-sum(p log2 p) for uniform A,C,G,T and for p=(0.7,0.1,0.1,0.1); compare to 2 bits. This single-symbol statistic ignores correlations and does not measure meaning or function.
18. **Generation:** compare repetitive and seeded pseudorandom strings compressed with zlib; record generator/seed, codec and input assumptions. Read Shuvaev abstract and first figure. Describe why an explicit wiring description is not a lower bound on a generative one. Optional: MIT chapter 23 on rate distortion; analogy to functional tolerance, not identical mathematics to TOST.
**Exit check:** Why does the genomic bottleneck not demonstrate DNA insufficiency for life or consciousness?
Optional historical reference: [Shannon 1948 PDF](https://web.mit.edu/6.441/spring05/reading/shannon1948.pdf).

## Unit 7 — Development and self-organization (supporting inquiry)
**Question:** How does a relatively compact inherited specification participate in generating many cell types and organized structures?
Required sources: [OpenStax 43.6 Early embryonic development](https://openstax.org/books/biology-2e/pages/43-6-fertilization-and-early-embryonic-development); [McColgan & DiFrisco 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11529278/); [OpenStax 16.4](https://openstax.org/books/biology-2e/pages/16-4-eukaryotic-transcription-gene-regulation).
19. **Experience:** compare embryonic stages and germ layers in 43.6. Draw genome + inherited cell + environment → development. A genome does not start with an empty cell.
20. **Local rules:** generate a binary branching structure for n=1,2,4,8; compare 2^n−1 nodes with a fixed branching rule and depth. Identify the interpreter and parameters. This is a toy, not embryology.
21. **Complexity:** choose two measurable dimensions (cell type diversity and regulatory connectivity, for example). Explain why gene count alone is inadequate; avoid treating species as a ladder. Propose a comparative test that accounts for phylogeny and annotation.
**Exit check:** Distinguish inherited information, developmentally acquired state and external inputs.

## Unit 8 — Biological intelligence, AI and responsible inquiry (Paper 3)
**Question:** What can the evolution of intelligent technology suggest about biology, without making unsupported equivalences?
Required sources: [Zador, 2019, A critique of pure learning PDF](https://repository.cshl.edu/id/eprint/38307/1/2019.Zador.ArtificialNeuralNetworks.pdf); [Dive into Deep Learning, free book/PDF](https://d2l.ai/), introductory neural-network and attention chapters only; [Messeri & Crockett, 2024, AI and illusions of understanding](https://www.crockettlab.org/ai-research); [Paper 3 v0.6](../papers/03-augmented-investigator/The_Augmented_Investigator_v0.6.md).
22. **Architecture vs learned parameters:** compute output of a tiny linear classifier before and after changing its weights. Read Zador introduction. Distinguish inherited circuit constraints, learning and experience.
23. **Scale and attention:** read the D2L chapter introducing attention; sketch how inputs receive different weights. Record one specific question motivated by AI development, plus an alternative biological mechanism. Do not infer consciousness from a model's behavior.
24. **Metacognition:** read Paper 3 sections 11.2, 12 and 12.2. Take one proposed research direction and choose integrate, contextualize, separate or defer; identify required evidence and what would refute it. Read Messeri & Crockett abstract and identify one risk in our own workflow.
**Exit check:** Can you distinguish a productive analogy, a measured finding, a validated inference, and a new question?

## Study record (copy one block after each session)
- Date / session:
- Phenomenon I observed:
- One sentence explaining the principle:
- What the example does NOT establish:
- One question to ask AI or a qualified specialist:
- Disposition: integrate / contextualize / separate / defer.

## Corrections and guardrails for prior collections
The original six-module Paper 2 course is preserved, but treat it as an optional detailed companion. A PWM log-odds score is not automatically binding energy; a null multiplicity result does not prove that backups protect gene output; negative epistasis does not prove saturation; phyloP conservation is not literally frozen DNA; chromosome holdout does not remove all sequence-similarity leakage; ±0.15 log2 corresponds to ratios 2^−0.15 to 2^0.15, not exactly symmetric percent changes. MPRA assay comparisons depend on study context and do not establish one platform is universally superior. Study the reported data with these qualifications.

## Resource provenance and status
Reconciles the existing Paper 2 foundations curriculum and the prior PDP-8/H100, enhancer, information-theory and evolutionary tracing discussions into one core route. The previous longer lists remain supplementary, not required. Source titles/landing pages were checked through web search on 26 November 2026 for the principal additions (OpenStax, DEC manual, Hopper, Whalen, Agarwal, McColgan/DiFrisco, MIT information theory, Shuvaev, Zador, Messeri/Crockett). A complete byte-level download or access audit of every linked resource has not been performed. PMC and institutional pages offer PDF controls where available; no promise that publisher PDFs are universally accessible. No third-party PDFs are redistributed here. No paid computing, hardware or journal subscription is required for the core learning path. No new manuscript revision or empirical result is claimed. Curriculum timing is an estimate, not a measured learning outcome.
