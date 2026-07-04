PROJECT: PPO cross-SOA structural bioinformatics pilot (Phase 1, PPO enzyme).

Before doing anything else, read these two files in this repo in full:
1. DECISION_LOG.md — why the project is scoped the way it is, and every correction 
   made to the working dataset so far. Do not re-derive or second-guess decisions 
   already recorded here; if something here seems inconsistent with the code or data 
   you find, flag it explicitly rather than silently resolving it.
2. PPO_Phase1_Final_Validated_Brief.md — the current, fully source-verified dataset: 
   confirmed mutations and accessions, the three-way numbering key (tobacco / 
   waterhemp / Palmer amaranth), the active-site residue reference hierarchy, 
   mechanism-class tags per mutation, and the exact validation-gate numbers your 
   pipeline needs to reproduce.

Also present in this repo: rangani_2019_table2_cross_resistance.csv (external 
validation dataset — real IC50/resistance-factor data for G399A, ΔG210, and R128L 
against 13 herbicides, common A. tuberculatus genetic background).

STATUS: domain sign-off is complete. All open questions from the original 
ppo_mutation_candidates.md sign-off request have been resolved and are recorded in 
DECISION_LOG.md section 5. Two items remain genuinely open (also in DECISION_LOG.md 
section 6): Giacomini 2017's accession numbers for R98G/R98M, and V361A's mechanism 
class. Do not attempt to resolve either by inference — flag them as open if they 
become blocking.

NEXT ACTIONS, IN ORDER:

1. Rebuild the mutation dataset to match PPO_Phase1_Final_Validated_Brief.md exactly 
   — including both ΔG210 accession pairs (ABD52326/ABD52328 and ABD52329/ABD52330), 
   the corrected V361A accessions (MH910646/MH910647, not QBB0236x), and the G399A 
   accessions (MK408971-MK408978).

2. Apply the three-way numbering key from the brief as a hard-coded reference — do 
   not recompute it from a fresh alignment.

3. Retrieve the 1SEZ structure (tobacco PPO2) from PDB. This is a real crystal 
   structure, not a homology-modeling target — use it directly as the template for 
   all downstream distance/accessibility calculations on the waterhemp and Palmer 
   amaranth sequences.

4. Run the alignment + numbering standardization step (originally Phase 1, Step 2), 
   now using the confirmed numbering key rather than deriving it fresh.

5. Script the ChimeraX distance-to-active-site (normalized, per the panel-review fix 
   in DECISION_LOG.md section 2) and solvent-accessibility calculations, using the 
   Heinemann 2007 four-residue core (Arg98, Phe392, Leu356, Leu372) as the primary 
   active-site reference.

6. Validation gate before scaling to any other enzyme: check whether your pipeline's 
   own calculations on WT vs. ΔG210 are directionally consistent with Dayan et al. 
   2010's numbers in the brief (cavity volume, FAD distance). This is the gate — do 
   not proceed to ALS/ACCase/EPSPS/HPPD until this checks out or discrepancies are 
   explained.

7. Tag ΔG210, G399A, and R98G/R98M with their mechanism_class fields per the brief. 
   Leave V361A's mechanism_class unset and flagged as open.

8. Report back: pipeline output for the ΔG210 validation gate, and any point where 
   the confirmed dataset doesn't match what's actually retrievable (e.g., if 1SEZ's 
   deposited sequence doesn't align cleanly with the numbering key as given).
