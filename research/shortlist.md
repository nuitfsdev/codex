# Thesis Research Shortlist

Project: 3D Scene Understanding with 2D Vision-Language Models via Abstract 3D Representations and Viewpoint Alignment

Last updated: 2026-09-07

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
Primary evidence: GraFT (arXiv:2609.03892, 2026-09-03), plus SceneGraphGrounder (arXiv:2605.21788) and ObsGraph (arXiv:2606.24068).

**Novelty boundary:** GraFT already performs training-free selective rendering/retrieval of referenced/query-relevant objects with GT-compatible 3D boxes and Qwen2.5-VL-7B/3B. SceneGraphGrounder already parses a query graph and performs relation-aware constrained graph matching for zero-shot 3D grounding. Therefore generic relevant-class extraction, query-graph construction, semantic candidate filtering, relation-aware matching of referred targets, and referenced-object-only rendering are baselines, not thesis novelty.

**Research Hypothesis:** open-ended ScanQA/SQA3D questions can require unnamed supporting/context objects beyond referred/query-graph entities. A support-aware selector that combines relation compatibility and co-visibility/evidence preservation can retain a minimal useful subscene, with PoseAlign-T used to refine viewpoint-dependent relations before Abstract-3D rendering.

**Current transfer rule:**
1. Build object table from fixed GT boxes: id, class, center, extent, optional color/RGB summary.
2. Parse explicit seed entities/attributes/relation intent; resolve plausible seed instances with synonyms/frozen semantic similarity. Hard-retain seeds and delay ambiguous same-class pruning.
3. Generate support candidates from cheap relation-compatible edges (near, above/below, support/contact, containment, overlap, functional/spatial cluster).
4. Add a co-visibility prior: objects repeatedly visible with seeds in informative views can enter even when their category is absent from the question.
5. Under a fixed object budget, use diversity-aware tie-breaking.
6. After PoseAlign-T, recompute viewpoint-dependent left/right/front/behind relations and prune incompatible supports.
7. Render only seed+support objects.

**Evaluation:** ScanQA/SQA3D downstream QA; Object Reduction Ratio; Question Entity Coverage; object-budget vs QA curve; Context Benefit Rate (Seed+Support correct while Seed-only fails); Support Ablation Sensitivity. Supporting-Context Retention is proxy-only unless an explicit support-object GT set is introduced.

**Core matched-budget ablation:** Full Scene vs GraFT-style Seed-only vs SceneGraphGrounder-style query-graph nodes vs Seed+KNN vs Seed+radius vs Seed+relation-aware support vs Seed+co-visibility vs Seed+relation+co-visibility vs +diversity vs +PoseAlign-T.

**Scores (1-5):** Novelty 3.5; Expected Accuracy Gain 3.5; Feasibility 4.5; Compute Cost 4.5 (higher=cheaper); Fit 5.0; Evidence Strength 4.5.
**Targets to test, not claims:** Object Reduction Ratio 50-85%; Question Entity Coverage >=95%; Supporting-Context Retention unknown/proxy-only; context-loss risk medium.
**Publication potential:** moderate-to-good only if matched-budget experiments show consistent QA preservation/gains specifically attributable to unnamed-support retention.

### 2. RCSX: Relation-Conditioned Supporting-Object Expansion
Sources: ReasoningGraph (ICRA 2026), View-on-Graph (AAAI 2026), SceneGraphGrounder (2026 preprint).

Role: strongest symbolic support generator inside SAFER-QA. SceneGraphGrounder lowers standalone novelty because query-graph relation matching is already prior art. Differentiation must be expansion beyond referred/query-graph nodes to unnamed QA evidence, under a strict rendering budget, followed by PoseAlign-T refinement.

Scores: Novelty 2.5 standalone / 3.5 inside SAFER-QA; Expected Accuracy Gain 3.5; Feasibility 4.5; Compute Cost 4.5; Fit 5.0; Evidence Strength 4.5.

### 3. CoVis-Support: Co-visibility/Evidence-Preserving Support Expansion
Source inspiration: ObsGraph (arXiv:2606.24068; under review), which organizes room-view-object evidence and explicitly preserves object co-visibility under bounded hierarchical retrieval.

Hypothesis: objects repeatedly co-visible with grounded seeds in informative views provide a training-free contextual prior complementary to geometry relations, improving unnamed-support retention over pure KNN/radius.

Rule: compute `score_cov(o)=sum_v w(v,q)*visible(seed,v)*visible(o,v)`, combine with geometry plausibility, retain candidates under the same object budget, then PoseAlign-T prune viewpoint-incompatible candidates.

Risks: incidental clutter, camera-coverage bias, large/frequent-object bias; should complement rather than replace relation-aware support.

Scores: Novelty 3.0 standalone / 3.5 inside SAFER-QA; Expected Accuracy Gain 3.5; Feasibility 4.5; Compute Cost 4.5; Fit 5.0; Evidence Strength 3.5.

### 4. OLT-QA Seed Retrieval Front End
Sources: AgentGrounder (ICRA 2026 workshops) plus GraFT.

Role: baseline/front end only. Build a lightweight object lookup table from GT boxes and use question parsing + synonyms/frozen semantics to identify seed/referred objects. Do not claim generic lookup, relevant-class extraction, or referred-object selection as novelty.

Scores: Novelty 1.5 standalone / 2.5 as component; Expected Accuracy Gain 3.0; Feasibility 4.5; Compute Cost 4.5; Fit 4.5; Evidence Strength 4.5.

### 5. Object-Diversity Context Preservation inspired by 3DZip
Source: 3DZip, ECCV 2026, arXiv:2608.01185; public code.

Use only as a support-budget tie-breaker after hard seed retention and support expansion; choose diverse supports rather than redundant nearest neighbors.

Scores: Novelty 3.0 integration; Expected Accuracy Gain 3.0; Feasibility 3.5; Compute Cost 4.0; Fit 4.0; Evidence Strength 4.0.

### 6. Question-Aligned View Selection after Subscene Selection
Sources: CoV (Findings ACL 2026), SpatialPrompting (Frontiers in Robotics and AI 2026), GraFT (2026 preprint), ViewMind3D (2026 preprint).

Strong precedent already exists. Treat as a secondary module/ablation: after SAFER-QA and PoseAlign-T, choose the smallest views jointly exposing retained seeds/supports.

Scores: Novelty 2.0; Expected Accuracy Gain 4.0; Feasibility 4.0; Compute Cost 3.5; Fit 4.5; Evidence Strength 5.0.

### 7. Post-selection Geometry-Aware Visual Token Pruning
Source: Seeing Once is Enough? Online Geometry-Aware Token Pruning for 3D QA (arXiv:2607.04079; ICLR 2026 workshop).

Role: efficiency ablation after selected-subscene multi-view rendering. Protect selected seed/support objects at object level and prune only redundant cross-view patches/tokens.

Scores: Novelty 2.0 standalone / 2.5 integration; Expected Accuracy Gain 3.0; Feasibility 4.0; Compute Cost 4.5; Fit 4.0; Evidence Strength 4.5.

## Evidence notes retained
- **GraFT (2026-09-03):** training-free 3DSG; GT ScanNet-compatible setting; query-relevant selective BEV; geometry-guided egocentric frame retrieval; Qwen2.5-VL-7B on ScanQA. Core near-task baseline.
- **SceneGraphGrounder (2026-05-20):** zero-shot query graph + semantic filtering + constrained relation graph matching; ScanRefer; preprint; code promised upon acceptance, not verified public 2026-09-07. Important novelty limiter for RCSX.
- **ObsGraph (2026-06-23):** room-view-object hierarchy, bounded coarse-to-fine retrieval, explicit co-visibility/raw-evidence preservation; under review; not ScanQA-specific. Motivation for CoVis-Support.
- **ViewMind3D (arXiv:2607.28442):** training-free question-driven multi-view selection + grounding + BEV + structured reasoning on ScanQA/SQA3D; strongest setup uses o3. Near-task baseline, not novelty.
- **TDVR (arXiv:2608.03763):** structured target/anchor/relation parsing and viewpoint-aware distractor resolution; seed-disambiguation precedent.
- **UniGround (arXiv:2603.08131):** training-free semantic candidate filtering + precision grounding; referred-target grounding, not unnamed support retention.
- **CoordRefer (arXiv:2608.05569):** evidence for resolving coordinate/reference frame before coordinate-dependent decisions, but requires SFT+GRPO.
- **SmartMage (arXiv:2608.05137):** query-adaptive evidence routing but trained; evidence only.

## Current top candidate
**SAFER-QA: Support-Aware Evidence Expansion for Selective Abstract 3D Rendering.**

Best current instantiation:
`seed retrieval -> relation-aware support + co-visibility support prior -> fixed-budget diversity selection -> PoseAlign-T directional refinement -> selective Abstract-3D render -> <=7B VLM`.

Reason: no 2026-09-06/07 paper found today supersedes GraFT. SceneGraphGrounder narrows the novelty boundary by making query-graph/relation matching a baseline, while ObsGraph adds independent evidence that co-visibility-preserving retrieval is useful under bounded context. The unresolved, thesis-relevant gap remains preserving **unnamed supporting/context evidence** for open-ended 3D QA while aggressively reducing the rendered object set.
