# Thesis Research Shortlist

Project: 3D Scene Understanding with 2D Vision-Language Models via Abstract 3D Representations and Viewpoint Alignment

Last updated: 2026-09-22

## Scope constraints
- Fixed ScanNet/ScanQA object annotations or 3D boxes as scene input.
- Detection/segmentation is not a thesis contribution.
- Prefer training-free / zero-shot / inference-only; 2D VLM <= ~7B where possible.
- Main pipeline: PoseRecover -> PoseAlign-T -> question-conditioned object/view selection -> 3D Abstract Renderer -> 2D VLM -> optional spatial verification / structured reasoning.
- Main object-selection method must not render the full scene.
- Seed/referred objects must be distinguished from unnamed supporting/context objects.
- Do not use ScanQA relevance/object IDs as selector supervision or as a presumed complete supporting-object GT set.

## Current weekly shortlist

### 1. SAFER-QA / QASER-Utility: QA-Utility-Aware Support Selection
Primary evidence: GraFT (arXiv:2609.03892), **PruneGround (EMNLP 2026 main; arXiv:2606.31148)**, SceneGraphGrounder (arXiv:2605.21788), SeGPruner (arXiv:2603.29437), and peer-reviewed active-perception grounding.

**Novelty boundary:** PruneGround is now a peer-reviewed first-tier novelty limiter. Its public pipeline already performs language-guided spatial pruning, target-anchor reformulation, local re-rendering, and explicitly emits `anchors_visual` for anchors absent from the original language. Generic language-conditioned pruning, unnamed-anchor discovery, target-anchor decomposition, or prune-then-render are therefore not defensible novelty claims.

**Remaining gap:** objects useful for open-ended QA may differ from objects useful for referential grounding. Test whether QA-specific retention of named seeds plus unnamed answer-support/context objects preserves ScanQA/SQA3D answers better than grounding-oriented pruning at the same object/render budget.

**Research Hypothesis:** a support selector optimized for downstream QA utility using relation compatibility and context/diversity reserves can improve the QA-vs-object-budget Pareto frontier over seed-only, KNN, and grounding-oriented pruning; PoseAlign-T then refines viewpoint-dependent relations before Abstract3D rendering.

**Transfer rule:**
1. Build object table from fixed GT boxes: id, class, center, extent, optional RGB summary.
2. Parse explicit seed entities/attributes/relation intent; hard-retain seeds and delay ambiguous same-class pruning.
3. Generate unnamed support candidates scene-wide from relation constraints and cheap box geometry; do not use distance as a universal hard gate.
4. Retain unnamed objects when they complete a relation constraint, disambiguate seed instances, provide answer evidence, or occupy a context/diversity reserve.
5. Under strict K, allocate support slots by QA evidence; optionally use uncertainty-gated expansion.
6. After PoseAlign-T, recompute left/right/front/behind and prune incompatible candidates.
7. Render only retained seed+support objects.

**Evaluation:** ScanQA/SQA3D downstream QA; Object Reduction Ratio; Question Entity Coverage; object-budget-vs-QA curve; Context Benefit Rate; Support Ablation Sensitivity; selected-object distribution and VLM-call budget for adaptive variants. Supporting-Context Retention remains proxy-only unless explicit support-object GT is introduced.

**Core matched-budget ablation:** Full Scene vs Seed-only vs Seed+KNN vs CAPruner vs PruneGround-inspired grounding pruning vs relation-aware support vs relation+diversity support vs uncertainty-gated expansion vs +PoseAlign-T; use K={5,10,20} where applicable.

**Scores (1-5):** Novelty **3.3**; Expected Accuracy Gain 3.6; Feasibility 4.6; Compute Cost 4.7 (higher=cheaper); Fit 5.0; Evidence Strength **4.9**.
**Targets to test, not claims:** Object Reduction Ratio 50-85%; Question Entity Coverage >=95%; Supporting-Context Retention unknown/proxy-only; context-loss risk medium.
**Publication potential:** moderate only if matched-budget experiments show a stable QA-support advantage over grounding-oriented pruning. Backbone scaling is baseline/ablation only.

### 2. RCSX: Relation-Conditioned Supporting-Object Expansion
Sources: ReasoningGraph (ICRA 2026), View-on-Graph (AAAI 2026), SceneGraphGrounder (2026 preprint).
Role: symbolic support generator inside QASER. Query-graph matching is prior art; differentiation must be QA-specific expansion beyond referred/query-graph nodes under strict render budget.
Scores: Novelty 2.5 standalone / 3.3 integration; Expected Accuracy Gain 3.5; Feasibility 4.5; Compute Cost 4.5; Fit 5.0; Evidence Strength 4.5.

### 3. OLEA: Object-Level Evidence Allocation
Source: SeGPruner (public code `intcomp/SegPruner`).
Role: saliency+geometric-diversity budget allocator after seed/support candidate generation, not standalone novelty.
Scores: Novelty 3.0 standalone / 3.5 integration; Expected Accuracy Gain 3.5; Feasibility 4.7; Compute Cost 4.8; Fit 5.0; Evidence Strength 4.6.

### 4. UGSE: Uncertainty-Gated Support Expansion
Source: Liang Geng, 3D visual grounding based on active perception, Complex & Intelligent Systems, published 2026-09-10.
Role: adaptive-budget refinement inside QASER. Start small, expand only for ambiguous/missing/conflicting evidence. Closed-loop evidence acquisition itself is prior art.
Scores: Novelty 3.0 standalone / 3.4 integration; Expected Accuracy Gain 3.5; Feasibility 4.2; Compute Cost 3.6; Fit 4.8; Evidence Strength 4.2.

### 5. CoVis-Support
Source inspiration: ObsGraph (arXiv:2606.24068).
Role: co-visibility prior/tie-breaker for support expansion; avoid requiring full-scene rendering in the main method.
Scores: Novelty 2.8 standalone / 3.3 integration; Expected Accuracy Gain 3.5; Feasibility 4.5; Compute Cost 4.5; Fit 5.0; Evidence Strength 3.5.

### 6. OLT-QA Seed Retrieval Front End
Sources: AgentGrounder, GraFT, PruneGround.
Role: baseline/front end only; question parsing + synonyms/frozen semantics over GT object table.
Scores: Novelty 1.3 standalone / 2.2 component; Expected Accuracy Gain 3.0; Feasibility 4.5; Compute Cost 4.5; Fit 4.5; Evidence Strength 4.7.

### 7. Object-Diversity Context Preservation
Source: 3DZip, ECCV 2026; public code.
Role: support-budget tie-breaker after seed retention/support expansion, not novelty headline.
Scores: Novelty 2.5 integration; Expected Accuracy Gain 3.0; Feasibility 3.5; Compute Cost 4.0; Fit 4.0; Evidence Strength 4.2.

### 8. Question-Aligned View Selection
Sources: CoV (Findings ACL 2026), GraFT, ViewMind3D, IVSGround, PruneGround MCDR.
Role: secondary module/ablation after subscene selection and PoseAlign-T. Strong prior art; do not claim question-conditioned view selection itself as novelty.
Scores: Novelty 1.6; Expected Accuracy Gain 4.0; Feasibility 4.0; Compute Cost 3.5; Fit 4.5; Evidence Strength 5.0.

## Evidence update — 2026-09-22
- **PruneGround:** arXiv v2 dated 2026-09-04 labels the paper `EMNLP 2026`; Jinesis Lab lists it among EMNLP 2026 main-conference papers. Public MIT repo implements top/oblique rendering, Qwen2.5-VL-3B LGSP, local side-view MCDR, and structured `anchors_visual`. This upgrades it from preprint-only to a peer-reviewed first-tier baseline/novelty limiter.
- Full PruneGround LLM-Grounder is not training-free; only its frozen pruning/reformulation ideas transfer cleanly to this thesis scope.
- Active-perception grounding remains evidence for adaptive local evidence acquisition but not QA-specific support selection.
- GraFT remains a near-task training-free ScanQA baseline; view selection is not a safe novelty claim.

## Current top candidate
**SAFER-QA / QASER-Utility: QA-specific retention of named + unnamed supporting objects before Abstract3D rendering under strict object/render budget.**

Best current instantiation:
`seed retrieval -> relation-conditioned scene-wide support candidates -> QA-utility/context allocation -> optional uncertainty expansion -> PoseAlign-T directional refinement -> selective Abstract3D render -> <=7B VLM`.

Reason: PruneGround's EMNLP 2026 status materially strengthens the evidence for spatial pruning while narrowing novelty. The key remaining testable distinction is **grounding utility vs QA support utility** at matched render budgets on ScanQA/SQA3D.
