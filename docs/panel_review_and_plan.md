# Panel Review & Claude Code Execution Plan
## Project: Cross-Site-of-Action Comparative Structural Bioinformatics

---

## Part A — Panel review

Five reviewers, each reading the proposal from their own angle. This is deliberately critical — the goal is to surface what a real peer reviewer would flag, before you spend six months building it.

### 1. Structural biologist

**What's solid:** The homology-modeling logic is exactly right, and better precedent exists than the original plan even knew. Plant PPO isn't a homology-modeling problem at all — there are five actual PPO crystal structures already solved, including tobacco mitochondrial PPO2 in complex with a herbicide inhibitor (Koch et al. 2004, PDB **1SEZ**), plus bacterial and human PPO structures. Even better: Franck Dayan (already on your collaborator list) co-authored a 2018 *Pest Management Science* paper — "Origins and structure of chloroplastic and mitochondrial plant protoporphyrinogen oxidases: implications for the evolution of herbicide resistance" — that did structural analysis of exactly the resistance mutations you'd be mapping, down to identifying a conserved active-site arginine substitution. That paper is your single best methodological template for the whole project, not just for PPO.

**What needs fixing — cross-enzyme distance comparability.** "Distance to active site" isn't directly comparable across ALS, PPO, ACCase, EPSPS, and HPPD, because these enzymes have wildly different sizes, pocket depths, and domain architectures. A mutation 8 Å from the active site in a small, compact enzyme might be structurally equivalent to one 20 Å away in a large multidomain enzyme like ACCase. **Fix:** normalize distance as a percentile rank within each protein's own distribution of residue-to-active-site distances, not as a raw Ångström value. Only the normalized version is a legitimate cross-enzyme comparison.

**What needs fixing — mutant structure prediction.** Running a mutant sequence through ColabFold to see how the mutation changes the fold does not work the way it might sound like it should. AlphaFold2-based tools predict structure primarily from evolutionary co-variation across a multiple sequence alignment; a single point mutation essentially never changes that signal enough to shift the predicted backbone, so a ColabFold prediction of a resistant mutant will come back looking almost identical to the wild type. This is a well-documented limitation, not a training or resource issue — it's *why* DeepMind built a separate model (AlphaMissense) specifically for point-mutation effect prediction, rather than just running AlphaFold twice. **Fix:** predict the wild-type structure once per target (via template or ColabFold), then evaluate each mutation's position *within that wild-type structure* — its distance to the active site, its solvent accessibility, its local packing environment — rather than trying to re-predict a mutant fold.

### 2. Weed science / resistance genetics reviewer

**The real bottleneck is curation, not compute.** Assembling a clean, correctly-numbered, correctly-sourced mutation list per enzyme is the most labor-intensive part of this project and the part most vulnerable to error — get the PPO2 G399A story (Amaranthus palmeri, Rangani et al.) right as your validation case, since it already combines molecular, computational, and biochemical evidence and gives you a built-in accuracy check.

**Sharpen the novelty claim.** "Resistance mutations tend to be near the active site" is expected, not surprising — it follows directly from basic enzyme biology you already know. What would make a reviewer sit up is the opposite finding: mutations that *don't* fit that pattern. Several documented ACCase and ALS resistance substitutions act allosterically rather than sitting directly in the pocket. **Recommendation:** explicitly hunt for and foreground any "outlier" mutations that fall outside the expected zone — that's the more citable result, and it's a genuine open question rather than a confirmation of something already assumed in your own manual's Part II.

### 3. Bioinformatics pipeline reviewer

**ConSurf won't scale the way the plan assumes.** ConSurf is a web-submission tool, one job at a time, with no public batch API — running it across six-plus targets and multiple species per target means a lot of manual submission-and-wait cycles. **Fix:** compute conservation directly and locally from your own multiple sequence alignment using a simple Shannon-entropy-per-column score (a few lines of Biopython) as the primary metric. This is fully automatable inside a Claude Code pipeline. Treat ConSurf as an optional manual spot-check on your pilot enzyme only, not a per-target dependency.

**Tooling ramp-up is underestimated.** Two to three weeks to get comfortable with ChimeraX/PyMOL scripting from a standing start is optimistic — budget four to six.

### 4. Biostatistician

**The proposed logistic regression has a class-imbalance and independence problem.** "Is this a known resistance position" versus "every other residue in the protein" produces a wildly imbalanced dataset (a handful of positives against hundreds of negatives), and residues within the same protein aren't independent observations. A naive pooled logistic regression here would draw exactly the kind of methods criticism that gets a paper sent back for revision. **Fix, preferred:** a permutation/enrichment test — for each enzyme, draw many random sets of residues equal in number to the known resistance positions, compute the same normalized-distance metric, and test whether the real resistance positions rank closer to the active site than the random draws. This sidesteps both the imbalance problem and the independence problem, and it's a natural fit for a Claude Code-scripted pipeline (this is just a for-loop with a random sample, repeated a few thousand times, per enzyme). If you want a regression framing at all, use enzyme identity as a random effect (a mixed model) rather than pooling everything into one fixed-effects model.

### 5. Journal-editor lens

**Fit:** *Pest Management Science* is the right first choice — it already publishes exactly this style of work (the Dayan 2018 paper is functionally a precedent in the same journal). *Frontiers in Plant Science* is a reasonable second choice but less targeted.

**What separates "accept" from "descriptive database paper" in review:** a sharp, falsifiable central claim. "We built annotated structures for six enzymes" is a resource, not a finding. "Resistance mutations across independently-evolved sites of action cluster in a statistically distinguishable structural zone, with identifiable exceptions, and the earliest lab-generated FAT/DHODH mutants already fall inside that zone" is a finding. Build the manuscript around the second framing from day one, not the first.

---

## Part B — Can Claude Code do this? Verdict: yes, with one hard boundary.

Claude Code (terminal, VS Code, or desktop) can write, run, debug, and iterate on essentially every *scripted* step in this revised pipeline: querying NCBI/UniProt/PDB APIs, running alignments, scripting ChimeraX for distance and solvent-accessibility calculations, computing entropy-based conservation, running the permutation test and any mixed models in R, generating figures, assembling the annotated dataset, managing the GitHub repo, and drafting write-up sections — provided the underlying software is installed and reachable from your machine (or Auburn's Linux server).

**The one thing it cannot do locally: the GPU-heavy neural network inference step (ColabFold), if you don't have GPU access.** ColabFold needs a GPU to run in any reasonable time, and a typical laptop doesn't have one suited to this. The practical workaround — used by essentially everyone without dedicated GPU hardware — is to run ColabFold in Google's free-tier Colab notebook by hand for each sequence that needs a de novo prediction (a few clicks, roughly 10–30 minutes per sequence on the free GPU), then hand the resulting PDB file back to Claude Code, which picks the pipeline back up from there exactly as if the structure had come from the AlphaFold database. This only affects targets without a good existing template or crystal structure — thanks to the PDB structures uncovered above, PPO, ALS/AHAS, ACCase, and EPSPS likely won't need this step at all; FAT and DHODH almost certainly will.

**What Claude Code doesn't replace:** the domain judgment calls — is this the right reference template, is this mutation list complete and correctly sourced, does this alignment look biologically sound. Claude Code will execute rigorously and flag anomalies, but those calls are still yours (or your collaborators').

---

## Part C — What you need to set up (your side, before Phase 0)

| Item | Notes |
|---|---|
| Claude Code | terminal, VS Code extension, or desktop app — your choice |
| ChimeraX | free download, full Python scripting API, actively maintained — recommended over PyMOL for this project |
| Python environment | `biopython`, `freesasa`, `pandas`, `requests` |
| R environment | you already have this from prior projects |
| Google account | for the free-tier ColabFold notebook (FAT/DHODH only) |
| NCBI account + API key (optional) | raises Entrez query rate limits; free, five-minute signup |
| Auburn mallard.auburn.edu access | you already have this — an alternative to your laptop for the heavier alignment/scripting steps if preferred |

---

## Part D — Phase-by-phase plan, marked by who does what

**Phase 0 — Setup (days 1–3)**
- **[You]** Install Claude Code and ChimeraX; confirm Python/R environments.
- **[Claude Code]** Scaffold the repo (`data/`, `scripts/`, `output/`), write `requirements.txt`/`environment.yml`, run smoke tests confirming each tool is reachable.

**Phase 1 — Pilot enzyme: PPO (weeks 1–3)**
Recommending PPO as the pilot rather than starting cold on ALS — you already have deep domain knowledge here, an actual crystal structure exists (1SEZ), and the Dayan 2018 paper gives you a direct benchmark to validate your pipeline against.
- **[Claude Code]** Pull PPO2 sequences (GenBank/UniProt) for *A. palmeri* and *A. tuberculatus*; retrieve 1SEZ from PDB; align weed sequences to the tobacco template.
- **[You]** Confirm the mutation list (ΔG210, G399A, R98L/R128L depending on numbering) against source papers, resolving numbering to one internal standard.
- **[Claude Code]** Script ChimeraX to compute distance-to-active-site (normalized) and solvent accessibility for each mutation position on the wild-type structure; compute entropy-based conservation from the alignment.
- **[Claude Code]** Run the permutation test for PPO alone as a first pass.
- **[You]** Sanity-check results against the Dayan 2018 paper's own structural conclusions — if your independently-built pipeline lands on a similar story for the conserved arginine substitution, that's your validation gate to proceed.

**Phase 2 — Established targets with existing structures: ALS/AHAS, ACCase, EPSPS, HPPD (weeks 4–10)**
- **[Claude Code]** Repeat the validated pilot pipeline per target, reusing the same scripts.
- **[You / collaborator]** Supply and sign off on each target's mutation list and template choice; this is where looping in a structural biology contact (Auburn Biological Sciences or HudsonAlpha) is most valuable.
- **[Claude Code]** Flag any target where template identity to the actual weed sequence is low, per the panel's concern above.

**Phase 3 — New targets: FAT, DHODH (weeks 10–14)**
- **[Claude Code]** Prepare FASTA inputs for any sequence lacking a usable template.
- **[You]** Run those sequences through the free ColabFold Colab notebook; download the resulting PDB files.
- **[Claude Code]** Resume the pipeline on those structures; map the known lab-generated resistant variants (FAT-A R171-region, the DHODH lab mutant) onto the now-established framework and generate the forward risk-read figure — your most citable result.

**Phase 4 — Cross-SOA synthesis (weeks 14–16)**
- **[Claude Code]** Pool all per-target tables; run the cross-enzyme permutation analysis; explicitly search for and report outlier/allosteric mutations per the panel's novelty note; generate final figures.
- **[You]** Draft the manuscript narrative around the sharpened central claim, with Claude Code drafting sections and you and Dr. Russell/collaborators reviewing.

**Phase 5 — Deposit and submit (weeks 16–18)**
- **[Claude Code]** Package the annotated dataset and all code into the GitHub repo; prepare the Zenodo deposit.
- **[You]** Submit to *Pest Management Science* first, given the direct precedent there.

---

## Part E — Assumptions I made — correct me if any are wrong

- Assumed you don't have dedicated GPU/HPC access for structure prediction and planned entirely around the free Colab tier for ColabFold. If you do have Auburn HPC GPU access, that step could be scripted more directly rather than done by hand.
- Assumed you're setting up Claude Code fresh. If you already have a preferred setup (terminal vs. VS Code vs. desktop), that just changes Phase 0's specifics, not the plan.
- Recommended **PPO as the pilot enzyme** rather than ALS — the opposite of what the earlier version of this plan suggested — specifically because the newly-confirmed 1SEZ crystal structure and the Dayan 2018 paper give you both a real structure and a direct external benchmark, on a target where your own domain expertise is already strongest. Say the word if you'd rather pilot on ALS instead (it also has solid structural precedent).
