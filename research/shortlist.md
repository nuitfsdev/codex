# Thesis Research Shortlist

Project: 3D Scene Understanding with 2D Vision-Language Models via Abstract 3D Representations and Viewpoint Alignment

Last updated: 2026-09-06

## Scope constraints
- Fixed ScanNet/ScanQA object annotations or 3D boxes as scene input.
- Detection/segmentation is not a thesis contribution.
- Prefer training-free / zero-shot / inference-only; 2D VLM <= ~7B where possible.
- Main pipeline: PoseRecover -> PoseAlign-T -> question-conditioned object/view selection -> 3D Abstract Renderer -> 2D VLM -> optional spatial verification / structured reasoning.
- Main object-selection method must not render the full scene.
- Seed/referred objects must be distinguished from unnamed supporting/context objects.
- Do not use ScanQA relevance/object IDs as selector supervision or as a presumed complete supporting-object GT set.

## Current weekly shortlist

### 1. SAFER-QA: Support-Aware Evidence Expansion for Selective Abstract 3D Rendering
Primary new evidence: **GraFT** (arXiv:2609.03892v1, submitted 2026-09-03; preprint; no verified official code as of 2026-09-06).

GraFT materially changes the novelty boundary. It is training-free, supports ground-truth ScanNet scene graphs, uses Qwen2.5-VL-7B/3B, and already renders only query-relevant/referenced objects. Its `RelevantClasses(q)` uses regex+synonyms or a VLM selector over scene classes. Therefore generic question->relevant-class extraction and referenced-object-only selective rendering are no longer plausible thesis novelties.

**Research Hypothesis:** GraFT-style referenced-object selection is incomplete for open-ended 3D QA because unnamed supporting/context objects can be required to answer. Starting from explicit seed objects, relation-conditioned support expansion can preserve a minimal useful evidence set, while PoseAlign-T can refine viewpoint-dependent relations before Abstract-3D rendering.

**Transfer rule:**
1. Build an object table from fixed GT boxes: id, class, center, extent, optional color/RGB summary.
2. Parse explicit seed entities, attributes and relation intent.
3. Resolve all plausible seed instances via class/synonym/frozen semantic similarity; hard-retain them and delay same-class disambiguation when ambiguous.
4. Expand unnamed supports through relation-compatible 1-hop graph edges; allow a second hop only for high-confidence chained relations.
5. Under a fixed object budget, use diversity-aware tie-breaking to avoid redundant KNN-style context.
6. After PoseAlign-T, recompute viewpoint-dependent left/right/front/behind relations and prune incompatible supports.
7. Render only seed+support objects.

**Supporting-context rule:** support objects need not occur as nouns in the question. Candidate supports can enter via near, above/below, support/contact, containment, overlap, or functional-cluster relations. Exact noun match must never be the sole inclusion rule.

**Evaluation:** downstream ScanQA/SQA3D QA; Object Reduction Ratio; Question Entity Coverage for explicit parsed entities; object-budget vs QA curve; Context Benefit Rate (Seed+Support correct while Seed-only fails); Support Ablation Sensitivity (QA drop when selected supports are removed). `Supporting-Context Retention` must be reported as a proxy unless an explicit support-object GT set is introduced.

**Core ablation:** Full Scene vs GraFT-style Seed-only vs Seed+KNN vs Seed+radius vs Seed+relation-aware support vs +diversity budget vs +PoseAlign-T, with matched object budgets.

**Scores (1-5):** Novelty 3.5; Expected Accuracy Gain 3.5; Feasibility 4.5; Compute Cost 4.5 (higher=cheaper); Fit 5.0; Evidence Strength 4.5.
**Object-selection targets to test, not claims:** Object Reduction Ratio 50-85%; Question Entity Coverage >=95% for explicit entities; Supporting-Context Retention unknown/proxy-only; context-loss risk medium.
**Publication potential:** moderate-to-good only if matched-budget experiments show consistent QA preservation/gains attributable specifically to unnamed-support retention.

### 2. OLT-QA Seed Retrieval Front End
Source inspiration: AgentGrounder (arXiv 2605.25901; ICRA 2026 MM-Spatial & SRRA Workshops; public code) plus GraFT.

Role after GraFT: **baseline/front end, not main novelty**. Build a lightweight object lookup table from GT boxes and use question parsing + synonyms/frozen semantics to identify seed/referred objects. Do not claim generic object lookup or relevant-class extraction as contribution.

Scores: Novelty 1.5 standalone / 2.5 as component; Expected Accuracy Gain 3.0; Feasibility 4.5; Compute Cost 4.5; Fit 4.5; Evidence Strength 4.5.

### 3. RCSX: Relation-Conditioned Supporting-Object Expansion
Source inspiration: Relationship-Aware Hierarchical 3D Scene Graph / ReasoningGraph (ICRA 2026) and View-on-Graph (AAAI 2026).

Hypothesis: after seeds are grounded, question-conditioned traversal over cheap GT-box relations can retain unnamed supporting evidence better than KNN/radius expansion at the same object budget.

This is now the strongest algorithmic submodule inside SAFER-QA. Scene-graph retrieval itself is not novel; the differentiator is QA-specific unnamed-support retention under an Abstract-3D rendering budget, followed by PoseAlign-T directional refinement.

Scores: Novelty 3.0 standalone / 3.5 inside SAFER-QA; Expected Accuracy Gain 3.5; Feasibility 4.5; Compute Cost 4.5; Fit 5.0; Evidence Strength 4.5.

### 4. Object-Diversity Context Preservation inspired by 3DZip
Source: 3DZip, ECCV 2026, arXiv 2608.01185; public code.

Use only as a support-budget tie-breaker: after hard seed retention and relation-aware candidate expansion, select a diverse subset of supports rather than redundant nearest neighbors. Do not make token compression the thesis core.

Scores: Novelty 3.0 integration; Expected Accuracy Gain 3.0; Feasibility 3.5; Compute Cost 4.0; Fit 4.0; Evidence Strength 4.0.

### 5. Question-Aligned View Selection after Subscene Selection
Sources: CoV (Findings ACL 2026), SpatialPrompting (Frontiers in Robotics and AI 2026), and GraFT (2026 preprint).

These establish strong precedent for question-conditioned/geometry-guided frame selection. Treat view selection as a secondary module/ablation: after SAFER-QA selects the subscene and PoseAlign-T establishes the reference frame, choose the smallest set of views that jointly exposes seeds and retained supports.

Scores: Novelty 2.0; Expected Accuracy Gain 4.0; Feasibility 4.0; Compute Cost 3.5; Fit 4.5; Evidence Strength 5.0.

### 6. Post-selection Geometry-Aware Visual Token Pruning
Source: Seeing Once is Enough? Online Geometry-Aware Token Pruning for 3D Question Answering (arXiv 2607.04079; ICLR 2026 workshop).

Role: efficiency ablation after selected-subscene multi-view rendering. Protect selected seed/support objects at object level; prune only redundant cross-view patches/tokens.

Scores: Novelty 2.0 standalone / 2.5 integration; Expected Accuracy Gain 3.0; Feasibility 4.0; Compute Cost 4.5; Fit 4.0; Evidence Strength 4.5.

## New critical evidence: GraFT (2026-09-03)
- Training-free framework over a compact 3D scene graph.
- Object nodes store class labels and 3D box geometry; ground-truth ScanNet annotations are explicitly evaluated as a perception setting.
- BEV module renders only query-relevant objects and omits the rest.
- `RelevantClasses(q)` uses regex+synonyms or a VLM selector; egocentric target objects are resolved by class name.
- ScanQA uses frozen Qwen2.5-VL-7B. Uniform 8-frame baseline CIDEr 58.0; selected top-1 69.2; top-2 73.6; top-3 75.9. Default top-2 also raises BLEU-1 22.2 -> 34.2.
- Qwen2.5-VL-3B is also demonstrated on VSI-Bench, strengthening fit with the <=7B constraint.
- Hardware/VRAM is not reported; no training is required.
- No official code repository was verified as of 2026-09-06.

**Novelty implication:** generic relevant-object extraction, selective BEV rendering of referenced objects, symbolic geometry over boxes, and geometry-guided view retrieval must be treated as prior work/baselines. The remaining promising gap is **support-aware selection of unnamed evidence for open-ended 3D QA under a strict object budget**.

## Evidence notes retained
- ViewMind3D (arXiv 2607.28442): training-free, question-driven multi-view selection + grounding + BEV + structured reasoning on ScanQA/SQA3D; strongest setup uses o3. Near-task baseline, not novelty.
- TDVR (arXiv 2608.03763): structured target/anchor/relation parsing and viewpoint-aware distractor resolution; useful seed disambiguation precedent.
- UniGround (arXiv 2603.08131): training-free semantic candidate filtering + precision grounding; referred-target grounding, not unnamed support retention.
- CoordRefer (arXiv 2608.05569): evidence for resolving coordinate/reference frame before coordinate-dependent decisions, but requires SFT+GRPO.
- SmartMage (arXiv 2608.05137): query-adaptive evidence routing but trained; evidence only.

## Current top candidate
**SAFER-QA: Support-Aware Evidence Expansion for Selective Abstract 3D Rendering.**

Reason: GraFT newly provides a near-direct, training-free baseline for selective rendering of *referenced* objects with ScanNet-compatible 3D boxes and Qwen2.5-VL-7B. That sharply reduces the novelty of OLT-style seed retrieval but strengthens the thesis case for the unresolved part: preserving **unnamed supporting/context objects** while aggressively reducing the rendered Abstract-3D subscene. The decisive experiment is now a matched-budget comparison of GraFT-style seed-only, KNN/radius expansion, relation-aware expansion, and relation+diversity expansion, followed by PoseAlign-T refinement and downstream QA preservation.
