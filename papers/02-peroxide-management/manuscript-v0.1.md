# Functional Continuity in Biological Evolution
## Hydrogen Peroxide Management as a Model of Architectural Conservation and Molecular Change

Randall S. Young, Ed.S. — Independent researcher — ORCID 0009-0003-1657-0243

**Developmental manuscript v0.1 — 27 November 2026. Not peer reviewed. Author-directed refocus; descriptive secondary analysis and prospective protocol. Not a submission-ready research article.**

### Abstract
Evolution can retain a functional outcome while modifying or replacing its molecular implementation. This established phenomenon motivates a more specific question: can architectural information improve prediction of the preservation of a defined functional capability beyond sequence conservation and simple component inventories? We develop hydrogen peroxide management as a coherent biological model. Typical heme catalase provides a chemically defined benchmark, while alternative scavenging pathways expose the distinction between an enzyme's capability and cellular protection. Previously archived descriptive analysis of sixteen purified catalases identifies approximately 15-fold variation in observed maximum turnover and 14,400-fold variation in heat-inactivation times at 65°C. A separate five-paralog dataset shows approximately 9.45-fold variation in specific activity. We add descriptive contrasts from a published bacterial peroxide-scavenging perturbation study: single-pathway losses produce different responses, and combined losses yield pronounced impairment. These examples demonstrate the value of distinguishing reaction identity, quantitative performance, and system-level resilience, but do not establish a new mechanism of evolutionary conservation. We propose held-out tests of structural and dependency-based predictors and specify the evidence required to draw evolutionary conclusions.

### 1. Introduction: the persistent requirement
Aerobic metabolism can generate hydrogen peroxide through unintended oxidation of cellular redox enzymes. Excess peroxide damages susceptible cellular components, whereas controlled peroxide also participates in signaling. The functional requirement is therefore not complete eradication of peroxide, but maintenance of exposure compatible with the organism's physiological context. Other protection, repair, diffusion and environmental conditions contribute; no single scavenging gene is universally necessary. The chemical hazard and a need for adequate control form the stable referent of the study.

The motivation originated in the PDP-8: an instruction-set contract endured across changing hardware implementations. The analogy suggests a useful question, not evidence of a shared mechanism. Natural selection, drift, duplication, horizontal transfer and convergence can all affect biological outcomes; evolution is not a designer with a predetermined goal. We test a bounded prediction about biological organization rather than reasserting already-known compensation or convergence.

### 2. Levels of functional continuity
1. Reaction identity: typical catalases dismutate 2 H2O2 into 2 H2O and O2.
2. Enzyme performance: reaction rate, substrate-dependent behavior and stability vary.
3. Cellular performance: a collection of scavengers, transport processes, regulation and repair must support a viable physiological exposure envelope.
4. Historical continuity: a phylogenetically grounded account must establish which features persisted, which changed, and whether similarities reflect descent or independent convergence.

These levels cannot be substituted for one another. Heme catalases, catalase-peroxidases and manganese catalases perform dismutation via distinct architectures. Peroxiredoxins and glutathione peroxidases reduce peroxide using reducing equivalents and require regeneration. They can contribute to the same cellular outcome without sharing the exact reaction stoichiometry. Protection depends on supply, expression, location and substrate concentration, not sequence annotation alone. [1–4]

### 3. Quantitative framework
For an idealized well-mixed compartment with fixed volume, let H be peroxide concentration, P endogenous production, J net exchange expressed as a concentration rate, and R_i removal rates:

dH/dt = P + J - sum_i R_i(H, state).

An illustrative removal curve is V_i H/(K_i+H), provided saturation kinetics are an appropriate approximation; this is not asserted as a universal catalase mechanism. V_i depends on enzyme abundance and activity; reducing equivalents, redox-regeneration capacity, regulation, pH and localization constrain effective removal. With nonnegative rates and stable steady conditions, balance means removal plus outward flux matches production plus inward flux. During perturbations peak exposure and duration also matter. In a simplified monotone model, removal at a specified upper bound must at least balance the net production there for the bound to be forward invariant; such a bound must be established biologically, not chosen arbitrarily. A fixed universal peroxide threshold is inappropriate.

The quantitative question is how different architectures satisfy a specified performance envelope across conditions, and how much their capabilities change when a component or shared dependency is lost. The framework distinguishes the engineering intuition from its empirical tests. Seaver and Imlay's published flux model already establishes the importance of quantifying production, removal and membrane transport [5]. This formulation is not presented as a novel kinetic model.

### 4. Data and methods: completed exploratory work
The immutable CAT-FEM v0.1 archive contains two transcribed enzyme cohorts and a Python descriptive baseline. Cohort A: 16 typical heme catalases purified in the 2002 study [6]; extract specific activity, observed maximum rate, concentration at half the observed maximum, heat-inactivation time. Cohort B: five paralogs from Streptomyces rimosus, characterized in 2021 [7]. Different protocols preclude pooling. The clade-median predictor is retrospective, leave-one-enzyme-out, with uneven groups (2/2/12). Raw replicate data and independent held-out cohorts are not established.

Cohort C: published E. coli perturbation study [8], Table 3 disk diffusion distance from disk edge and separate extracellular peroxide measurements reported in the text; Table 2 reporter activity is analyzed separately. We compute descriptive contrasts from the published means. A disk inhibition zone is an indirect phenotype, not a linear measurement of catalytic activity or fitness. Detection-limited observations are censored, not zeros. No p-values, equivalence classifications or confidence intervals are inferred from these summary values.

### 5. Results: biochemical benchmark
| Property (2002 cohort) | Minimum | Maximum | Fold range |
|---|---:|---:|---:|
| Specific activity (U/mg) | 20,700 | 273,800 | 13.23 |
| Observed maximum per heme per second | 54,000 | 833,000 | 15.43 |
| Half observed maximum concentration (mM) | 38 | 599 | 15.76 |
| Time to 50% inactivation at 65°C (min) | 0.05 | 720 | 14,400 |

The panel was selected for characterized catalases: it does not estimate the fraction of all sequence variants preserving function. These results reproduce the broad variability already documented by the original investigators. Clade-based prediction improves specific activity error by about 40%, worsens observed maximum-rate error by about 24%, and improves the other two endpoints by about 19% and 6%, respectively. These are exploratory prior calculations, not independent validation. The five-paralog cohort shows 9.45-fold specific activity and 5.28-fold apparent turnover ranges. Sequence and structure matching remain uncompleted.

### 6. Results: a functional system rather than an enzyme
In a published E. coli study [8], catalase-null and Ahp-null strains retain substantial scavenging at a low peroxide challenge, while the strain lacking both catalases and Ahp has very little. Ahp loss induces catalase via the OxyR regulon; catalase is more important under the higher exposure tested. Combined deficiency impairs aerobic growth. These are published findings, not new experiments by this project.

| Genotype (deleted genes) | Inhibition-zone distance (cm) |
|---|---:|
| Wild type | 1.1 |
| katG | 1.6 |
| ahpCF | 1.1 |
| katG katE | 1.6 |
| ahpCF katG | 2.9 |
| ahpCF katG katE | 3.1 |

The descriptive additive-distance interaction for katG and ahpCF loss is 2.9 - 1.6 - 1.1 + 1.1 = 1.3 cm. The scale is a diffusion phenotype, so this is not an estimate of biochemical epistasis or an inferential test. In a separate growth experiment the triple mutant's extracellular peroxide reached 1.8 µM, versus values below approximately 0.04 µM for wild type and the two single-pathway deficient strains: 45 times the approximate detection limit, not a measured fold difference between two concentrations. In Table 2, aerobic reporter activity in Ahp-null OxyR-positive cells is 0.35 vs 0.03 U/mg for the isogenic control; extracellular catalase reduces the former to 0.18. The reported means and SDs are source data; the ratios (~11.7 and ~49% reduction) are descriptive. Reporter output reflects regulatory induction rather than a direct peroxide concentration.

These observations make complementarity and feedback experimentally tangible. They also show why a component inventory is inadequate: activity changes after perturbation, effectiveness depends on concentration, and external and internal exposures differ. They do not demonstrate historical evolutionary substitution in E. coli.

### 7. Prospective hypotheses
H-P1: within a homologous catalase family, prespecified structure features add out-of-sample predictive information about measured enzyme performance beyond sequence, phylogeny and assay baselines.
H-P2: condition-specific complementary scavenging capacities and regulatory/reducing-equivalent dependencies add predictive information about organism-level protection beyond total capacity and exposure alone.
H-P3: in independently sampled lineages, changes in implementations can occur while a biologically specified protective envelope is retained; test only after comparable phenotype and phylogenetic data are identified.

The accompanying PROTOCOL.md specifies data requirements, held-out grouping, falsification and release gates. Do not present these hypotheses as results. If no suitable external data exist, restrict the manuscript to a clearly labeled conceptual and exploratory contribution.

### 8. Discussion
The chemical task and the organism-level task are related but distinct. Different catalases perform the same reaction with widely different observed operating properties. Complementary pathways can maintain removal under changing conditions, but feedback may depend on shared regulators or reducing-equivalent supply. The system may also trade energy cost, response time, localization and signaling against protective capacity. A molecular structure or sequence can be conserved for reasons unrelated to the endpoint under investigation. The incremental contribution, if confirmed, would be an independently validated architectural prediction—not the observation that catalases are ancient or that compensation occurs.

The central example is deliberately narrower than the former primate-enhancer manuscript. The latter remains a separate companion with its own assays, null results, and limitations. No enhancer data are pooled or repurposed as catalase validation. The kitchen inquiry is an educational antecedent, not primary experimental evidence: crude tissues differ in enzyme abundance, other constituents, mass transfer and foam formation. No wet-lab measurements by this investigator are asserted.

### 9. Limitations and conclusion
The current cohorts are small, selected and dependent; kinetic conditions differ; raw uncertainty and exact construct matches remain incomplete. The bacterial example is a single organism and cannot establish ancient ancestry. Literature already describes catalytic diversity, convergence and compensatory scavenging. These established findings are positive controls for the research design. They do not prove the prospective hypotheses or generalize to the origin of life.

The study reframes the original C2G question as a measurable problem: what capability must persist, what can vary, and what is sufficient under specified conditions? A useful empirical contribution will require predictive validation beyond existing knowledge. This v0.1 draft defines that task without concealing earlier failures or claiming unperformed experiments.

### References
1. Zamocky M, Furtmüller PG, Obinger C. Evolution of catalases from bacteria to humans. 2008. https://doi.org/10.1089/ars.2008.2046
2. Imlay JA. Cellular defenses against superoxide and hydrogen peroxide. 2008. https://pmc.ncbi.nlm.nih.gov/articles/PMC3057177/
3. The biological chemistry of hydrogen peroxide. 2013. https://pubmed.ncbi.nlm.nih.gov/23849856/
4. Hydrogen peroxide as a central redox signaling molecule in physiological oxidative stress. 2017. https://pmc.ncbi.nlm.nih.gov/articles/PMC5256672/
5. Seaver LC, Imlay JA. Hydrogen peroxide fluxes and compartmentalization inside growing Escherichia coli. 2001. https://doi.org/10.1128/JB.183.24.7182-7189.2001
6. Switala J, Loewen PC. Diversity of properties among catalases. 2002. https://pubmed.ncbi.nlm.nih.gov/12054464/
7. The Richness and Diversity of Catalases in Bacteria. 2021. https://doi.org/10.3389/fmicb.2021.645477
8. Seaver LC, Imlay JA. Alkyl hydroperoxide reductase is the primary scavenger of endogenous hydrogen peroxide in Escherichia coli. 2001. https://doi.org/10.1128/JB.183.24.7173-7181.2001

### Reproducibility and declarations
See CAT-FEM v0.1, ecoli_2001.csv, analyze_system.py, SYSTEM_RESULTS.json, PROTOCOL.md, and the preservation decision record. AI-assisted drafting and secondary analysis; author review and independent specialist review pending. No claim of new biological sampling, laboratory validation or funding declaration. Author to approve declarations before submission.
