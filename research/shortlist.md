# Thesis Research Shortlist

Project: 3D Scene Understanding with 2D Vision-Language Models via Abstract 3D Representations and Viewpoint Alignment

Last updated: 2026-09-24

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
Primary evidence: GraFT (arXiv:2609.03892), PruneGround (EMNLP 2026 main; arXiv:2606.31148), SparseTalk (arXiv:2609.15137), SceneBench (arXiv:2609.16233), SceneGraphGrounder, SeGPruner, and peer-reviewed active-perception grounding.

**Novelty boundary:** generic language-conditioned pruning, unnamed-anchor discovery, target-anchor decomposition, prune-then-render, object-aware sparsification, generic context retention, hierarchical context, or multi-level reasoning are not defensible novelty claims.

**Remaining gap:** objects useful for open-ended QA may differ from objects useful for referential grounding or question-independent scene compression. Test whether QA-specific retention of named seeds plus unnamed answer-support/context objects preserves ScanQA/SQA3D answers better than grounding-oriented pruning and question-independent object coverage at the same object/render budget.

**Research Hypothesis:** a support selector optimized for downstream QA utility using relation compatibility plus a small context reserve can improve the QA-vs-object-budget Pareto frontier over seed-only, KNN, semantic Top-K, question-independent object coverage, and grounding-oriented pruning; PoseAlign-T then refines viewpoint-dependent relations before Abstract3D rendering.

**Transfer rule:**
1. Build object table from fixed GT boxes: id, class, center, extent, optional RGB summary.
2. Parse explicit seed entities/attributes/relation intent; hard-retain seeds and delay ambiguous same-class pruning.
3. Generate unnamed support candidates scene-wide from relation constraints and cheap box geometry; do not use distance as a universal hard gate.
4. Retain unnamed objects when they complete a relation constraint, disambiguate seed instances, provide answer evidence, or occupy a context/diversity reserve.
5. Under strict K, allocate support slots by QA evidence; test 10/20/30% context reserve and optionally uncertainty-gated expansion.
6. After PoseAlign-T, recompute left/right/front/behind and prune incompatible candidates.
7. Render only retained seed+support objects.

**Evaluation:** ScanQA/SQA3D downstream QA; Object Reduction Ratio; Question Entity Coverage; object-budget-vs-QA curve; Context Benefit Rate; Support Ablation Sensitivity; selected-object distribution and VLM-call budget for adaptive variants. Supporting-Context Retention remains proxy-only unless explicit support-object GT is introduced.

**Core matched-budget ablation:** Full Scene vs question-independent object coverage vs Seed-only vs Seed+KNN vs SemanticTopK vs CAPruner vs PruneGround-inspired grounding pruning vs relation-aware QA support vs QA support + context reserve vs uncertainty-gated expansion vs +PoseAlign-T; use K={5,10,20} where applicable.

**Scores (1-5):** Novelty 3.3; Expected Accuracy Gain 3.7; Feasibility 4.7; Compute Cost 4.8 (higher=cheaper); Fit 5.0; Evidence Strength 4.9.
**Targets to test, not claims:** Object Reduction Ratio 50-85%; Question Entity Coverage >=95%; Supporting-Context Retention unknown/proxy-only; context-loss risk medium.
**Publication potential:** moderate only if matched-budget experiments show a stable QA-support advantage over both grounding-oriented pruning and question-independent object coverage. Backbone scaling is baseline/ablation only.

### 2. RCSX: Relation-Conditioned Supporting-Object Expansion
Role: symbolic support generator inside QASER. Query-graph matching is prior art; differentiation must be QA-specific expansion beyond referred/query-graph nodes under strict render budget.
Scores: Novelty 2.5 standalone / 3.3 integration; Expected Accuracy Gain 3.5; Feasibility 4.5; Compute Cost 4.5; Fit 5.0; Evidence Strength 4.5.

### 3. QASER-BC: Budgeted Context Reserve
Source: SparseTalk (arXiv:2609.15137; preprint, 2026-09-14).
Role: refinement inside QASER. After hard-retaining seeds and QA-support candidates, reserve 10/20/30% of K for context/object coverage. SparseTalk is question-independent and token-level; this thesis tests question-conditioned object-level pre-render allocation.
Scores: Novelty 3.1 standalone / 3.5 integration; Expected Accuracy Gain 3.7; Feasibility 4.8; Compute Cost 4.9; Fit 5.0; Evidence Strength 4.8.

### 4. H-QASER: Hierarchical Support Expansion
Source: SceneBench (arXiv:2609.16233; preprint, submitted 2026-09-14).
Role: optional refinement inside QASER. Use coarse room/functional-group relevance to allocate support slots while retaining scene-wide relation candidates and a cross-group reserve. Do not make hierarchy generation a core contribution because ScanQA/SQA3D lack SceneBench-style hierarchy and hierarchical reasoning is prior art.
Scores: Novelty 2.8 standalone / 3.4 integration; Expected Accuracy Gain 3.7; Feasibility 4.0; Compute Cost 4.7; Fit 4.6; Evidence Strength 4.6.

### 5. OLEA: Object-Level Evidence Allocation
Role: saliency+geometric-diversity budget allocator after seed/support candidate generation, not standalone novelty.
Scores: Novelty 3.0 standalone / 3.5 integration; Expected Accuracy Gain 3.5; Feasibility 4.7; Compute Cost 4.8; Fit 5.0; Evidence Strength 4.6.

### 6. UGSE: Uncertainty-Gated Support Expansion
Role: adaptive-budget refinement inside QASER. Start small, expand only for ambiguous/missing/conflicting evidence. Closed-loop evidence acquisition itself is prior art.
Scores: Novelty 3.0 standalone / 3.4 integration; Expected Accuracy Gain 3.5; Feasibility 4.2; Compute Cost 3.6; Fit 4.8; Evidence Strength 4.2.

### 7. CoVis-Support
Role: co-visibility prior/tie-breaker for support expansion; avoid requiring full-scene rendering in the main method.
Scores: Novelty 2.8 standalone / 3.3 integration; Expected Accuracy Gain 3.5; Feasibility 4.5; Compute Cost 4.5; Fit 5.0; Evidence Strength 3.5.

### 8. OLT-QA Seed Retrieval Front End
Role: baseline/front end only; question parsing + synonyms/frozen semantics over GT object table.
Scores: Novelty 1.3 standalone / 2.2 component; Expected Accuracy Gain 3.0; Feasibility 4.5; Compute Cost 4.5; Fit 4.5; Evidence Strength 4.7.

### 9. Question-Aligned View Selection
Role: secondary module/ablation after subscene selection and PoseAlign-T. Strong prior art; do not claim question-conditioned view selection itself as novelty.
Scores: Novelty 1.6; Expected Accuracy Gain 4.0; Feasibility 4.0; Compute Cost 3.5; Fit 4.5; Evidence Strength 5.0.

## Evidence update — 2026-09-24
- **SceneBench (arXiv:2609.16233):** submitted 2026-09-14; current status verified as arXiv preprint. It provides 966 photorealistic indoor scenes, >183K hierarchical nodes with text descriptions and 3D boxes, and 33,524 QA pairs. Its hierarchy spans scene -> room -> functional area -> object group -> object.
- SceneBench's grounded QRA tasks explicitly require evidence acquisition across semantic levels, including target and adjacent/supporting objects. This strengthens the motivation for retaining unnamed context rather than exact-noun-only or seed-local selection.
- SceneBench is not a direct replacement for ScanQA/SQA3D because its scene representation and hierarchy differ. Use it as evidence and possibly an auxiliary stress-test, not the primary benchmark.
- No new 2026-09-23/24 paper found in today's scan directly displaced QASER-Utility.
- Novelty boundary tightened: generic hierarchical context/multi-level reasoning is not a sufficient contribution. The key claim remains QA-conditioned pre-render retention under strict object/render budget.

## Current top candidate
**SAFER-QA / QASER-Utility: QA-specific retention of named + unnamed supporting objects before Abstract3D rendering under strict object/render budget.**

Best current instantiation:
`seed retrieval -> relation-conditioned scene-wide support candidates -> QA-utility allocation + small context reserve -> optional hierarchy/context prior -> optional uncertainty expansion -> PoseAlign-T directional refinement -> selective Abstract3D render -> <=7B VLM`.

Reason: SceneBench strengthens the case that compositional 3D QA often needs evidence beyond explicit question nouns and flat object-level relevance, but it does not solve question-conditioned pre-render object selection for ScanQA/SQA3D. The remaining defensible test is whether QA-conditioned support selection achieves a better QA-vs-object-budget frontier than grounding-oriented pruning and question-independent coverage.
