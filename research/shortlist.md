# Thesis Research Shortlist

Project: 3D Scene Understanding with 2D Vision-Language Models via Abstract 3D Representations and Viewpoint Alignment

Last updated: 2026-09-08

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
Primary evidence: GraFT (arXiv:2609.03892, 2026-09-03), SceneGraphGrounder (arXiv:2605.21788), ObsGraph (arXiv:2606.24068), and SeGPruner (arXiv:2603.29437).

**Novelty boundary:** GraFT already performs training-free selective rendering/retrieval of referenced/query-relevant objects with GT-compatible 3D boxes and Qwen2.5-VL-7B/3B. SceneGraphGrounder already parses a query graph and performs relation-aware constrained graph matching for zero-shot 3D grounding. SeGPruner already shows on ScanQA that semantic saliency plus explicit 3D geometric diversity is an effective training-free budget-allocation principle at visual-token level. Therefore generic relevant-class extraction, query-graph construction, semantic candidate filtering, relation-aware matching of referred targets, referenced-object-only rendering, and semantic+geometry token pruning are baselines, not thesis novelty.

**Research Hypothesis:** open-ended ScanQA/SQA3D questions can require unnamed supporting/context objects beyond referred/query-graph entities. A support-aware object selector that combines relation compatibility, co-visibility/evidence preservation, and explicit geometric diversity under a fixed object budget can retain a minimal useful subscene, with PoseAlign-T used to refine viewpoint-dependent relations before Abstract-3D rendering.

**Current transfer rule:**
1. Build object table from fixed GT boxes: id, class, center, extent, optional color/RGB summary.
2. Parse explicit seed entities/attributes/relation intent; resolve plausible seed instances with synonyms/frozen semantic similarity. Hard-retain seeds and delay ambiguous same-class pruning.
3. Generate support candidates from cheap relation-compatible edges (near, above/below, support/contact, containment, overlap, functional/spatial cluster).
4. Add a co-visibility prior: objects repeatedly visible with seeds in informative views can enter even when their category is absent from the question.
5. Under a fixed object budget, allocate support capacity between high semantic/relation evidence and spatially diverse context rather than using a single Top-K/KNN criterion.
6. After PoseAlign-T, recompute viewpoint-dependent left/right/front/behind relations and prune incompatible supports.
7. Render only seed+support objects.

**Evaluation:** ScanQA/SQA3D downstream QA; Object Reduction Ratio; Question Entity Coverage; object-budget vs QA curve; Context Benefit Rate (Seed+Support correct while Seed-only fails); Support Ablation Sensitivity. Supporting-Context Retention is proxy-only unless an explicit support-object GT set is introduced.

**Core matched-budget ablation:** Full Scene vs GraFT-style Seed-only vs SceneGraphGrounder-style query-graph nodes vs Seed+KNN vs Seed+radius vs Seed+relation-aware support vs Seed+co-visibility vs Seed+spatial-diversity vs Seed+relation+co-visibility vs Seed+relation+diversity vs Seed+relation+co-visibility+diversity vs +PoseAlign-T.

**Scores (1-5):** Novelty 3.7; Expected Accuracy Gain 3.6; Feasibility 4.6; Compute Cost 4.7 (higher=cheaper); Fit 5.0; Evidence Strength 4.7.
**Targets to test, not claims:** Object Reduction Ratio 50-85%; Question Entity Coverage >=95%; Supporting-Context Retention unknown/proxy-only; context-loss risk medium.
**Publication potential:** moderate-to-good only if matched-budget experiments show consistent QA preservation/gains specifically attributable to unnamed-support retention and dual evidence allocation at object level.

### 2. RCSX: Relation-Conditioned Supporting-Object Expansion
Sources: ReasoningGraph (ICRA 2026), View-on-Graph (AAAI 2026), SceneGraphGrounder (2026 preprint).

Role: strongest symbolic support generator inside SAFER-QA. SceneGraphGrounder lowers standalone novelty because query-graph relation matching is already prior art. Differentiation must be expansion beyond referred/query-graph nodes to unnamed QA evidence, under a strict rendering budget, followed by PoseAlign-T refinement.

Scores: Novelty 2.5 standalone / 3.5 inside SAFER-QA; Expected Accuracy Gain 3.5; Feasibility 4.5; Compute Cost 4.5; Fit 5.0; Evidence Strength 4.5.

### 3. OLEA: Object-Level Evidence Allocation inspired by SeGPruner
Source: SeGPruner (arXiv:2603.29437; public code `intcomp/SegPruner`).

Hypothesis: move SeGPruner's saliency-plus-geometric-diversity principle one level earlier, from visual-token pruning to GT-object budget allocation. Hard-retain seeds, rank relation/semantic support candidates, reserve some budget for spatially diverse context, then PoseAlign-T prune viewpoint-incompatible candidates before rendering.

Role: budget allocator inside SAFER-QA, not a standalone novelty claim. Direct ScanQA evidence supports the underlying principle: SeGPruner is training-free, uses LLaVA-OneVision-Qwen2-7B, and reports aggressive token reduction with competitive QA and large latency savings.

Risks: object-level saliency is not equivalent to token attention; diversity can retain distant clutter; gains may disappear when relation-aware support already provides enough coverage.

Scores: Novelty 3.0 standalone / 3.7 inside SAFER-QA; Expected Accuracy Gain 3.5; Feasibility 4.7; Compute Cost 4.8; Fit 5.0; Evidence Strength 4.6.

### 4. CoVis-Support: Co-visibility/Evidence-Preserving Support Expansion
Source inspiration: ObsGraph (arXiv:2606.24068; under review), which organizes room-view-object evidence and explicitly preserves object co-visibility under bounded hierarchical retrieval.

Hypothesis: objects repeatedly co-visible with grounded seeds in informative views provide a training-free contextual prior complementary to geometry relations, improving unnamed-support retention over pure KNN/radius.

Rule: compute `score_cov(o)=sum_v w(v,q)*visible(seed,v)*visible(o,v)`, combine with geometry plausibility, retain candidates under the same object budget, then PoseAlign-T prune viewpoint-incompatible candidates.

Risks: incidental clutter, camera-coverage bias, large/frequent-object bias; should complement rather than replace relation-aware support.

Scores: Novelty 3.0 standalone / 3.5 inside SAFER-QA; Expected Accuracy Gain 3.5; Feasibility 4.5; Compute Cost 4.5; Fit 5.0; Evidence Strength 3.5.

### 5. OLT-QA Seed Retrieval Front End
Sources: AgentGrounder (ICRA 2026 workshops) plus GraFT.

Role: baseline/front end only. Build a lightweight object lookup table from GT boxes and use question parsing + synonyms/frozen semantics to identify seed/referred objects. Do not claim generic lookup, relevant-class extraction, or referred-object selection as novelty.

Scores: Novelty 1.5 standalone / 2.5 as component; Expected Accuracy Gain 3.0; Feasibility 4.5; Compute Cost 4.5; Fit 4.5; Evidence Strength 4.5.

### 6. Object-Diversity Context Preservation inspired by 3DZip
Source: 3DZip, ECCV 2026, arXiv:2608.01185; public code.

Use only as a support-budget tie-breaker after hard seed retention and support expansion; choose diverse supports rather than redundant nearest neighbors. SeGPruner now provides more direct ScanQA evidence for the same general principle of balancing salient evidence with geometric diversity.

Scores: Novelty 2.7 integration; Expected Accuracy Gain 3.0; Feasibility 3.5; Compute Cost 4.0; Fit 4.0; Evidence Strength 4.2.

### 7. Question-Aligned View Selection after Subscene Selection
Sources: CoV (Findings ACL 2026), SpatialPrompting (Frontiers in Robotics and AI 2026), GraFT (2026 preprint), ViewMind3D (2026 preprint), IVSGround (arXiv:2609.04741; ECCV 2026 evidence).

Strong precedent already exists. IVSGround further narrows novelty by learning query-conditioned influential views per candidate object and showing clear grounding gains, but its reported pipeline uses a LoRA-fine-tuned Qwen3-VL-8B selector and Qwen3-VL-32B reasoning VLM, so it is not suitable as the main method under the preferred training-free / <=7B constraint. Treat view selection as a secondary module/ablation: after SAFER-QA and PoseAlign-T, choose the smallest views jointly exposing retained seeds/supports.

Scores: Novelty 1.8; Expected Accuracy Gain 4.0; Feasibility 4.0 for training-free heuristic variant; Compute Cost 3.5; Fit 4.5; Evidence Strength 5.0.

### 8. Post-selection Geometry-Aware Visual Token Pruning
Sources: Seeing Once is Enough? Online Geometry-Aware Token Pruning for 3D QA (arXiv:2607.04079; ICLR 2026 workshop) and SeGPruner (arXiv:2603.29437; public code).

Role: efficiency ablation after selected-subscene multi-view rendering. Protect selected seed/support objects at object level and prune only redundant cross-view patches/tokens. SeGPruner is the stronger direct ScanQA baseline because it combines semantic saliency with geometry-guided spatial diversity on LLaVA-OneVision-Qwen2-7B.

Scores: Novelty 1.8 standalone / 2.3 integration; Expected Accuracy Gain 3.0; Feasibility 4.0; Compute Cost 4.5; Fit 4.2; Evidence Strength 4.8.

## Evidence notes retained
- **GraFT (2026-09-03):** training-free 3DSG; GT ScanNet-compatible setting; query-relevant selective BEV; geometry-guided egocentric frame retrieval; Qwen2.5-VL-7B on ScanQA. Core near-task baseline.
- **SeGPruner (2026-03-31):** training-free semantic+geometry visual-token pruning; ScanQA/OpenEQA; public code; LLaVA-OneVision-Qwen2-7B; reports up to 91% token reduction and 86% latency reduction. Strong evidence for dual evidence allocation, but at token rather than object level.
- **IVSGround / Where to Look Matters (2026-09-04):** learned query-conditioned influential view selection for 3D grounding; ScanRefer/NR3D; reported Qwen3-VL-8B LoRA view selector + Qwen3-VL-32B reasoning VLM. Novelty limiter for view selection; not main-method fit.
- **SceneGraphGrounder (2026-05-20):** zero-shot query graph + semantic filtering + constrained relation graph matching; ScanRefer; preprint; code promised upon acceptance, not verified public 2026-09-08. Important novelty limiter for RCSX.
- **ObsGraph (2026-06-23):** room-view-object hierarchy, bounded coarse-to-fine retrieval, explicit co-visibility/raw-evidence preservation; under review; not ScanQA-specific. Motivation for CoVis-Support.
- **ViewMind3D (arXiv:2607.28442):** training-free question-driven multi-view selection + grounding + BEV + structured reasoning on ScanQA/SQA3D; strongest setup uses o3. Near-task baseline, not novelty.
- **TDVR (arXiv:2608.03763):** structured target/anchor/relation parsing and viewpoint-aware distractor resolution; seed-disambiguation precedent.
- **UniGround (arXiv:2603.08131):** training-free semantic candidate filtering + precision grounding; referred-target grounding, not unnamed support retention.
- **CoordRefer (arXiv:2608.05569):** evidence for resolving coordinate/reference frame before coordinate-dependent decisions, but requires SFT+GRPO.
- **SmartMage (arXiv:2608.05137):** query-adaptive evidence routing but trained; evidence only.

## Current top candidate
**SAFER-QA: Support-Aware Evidence Expansion for Selective Abstract 3D Rendering.**

Best current instantiation:
`seed retrieval -> relation-aware support + co-visibility support prior -> fixed-budget semantic/relation + spatial-diversity allocation -> PoseAlign-T directional refinement -> selective Abstract-3D render -> <=7B VLM`.

Reason: SeGPruner adds direct ScanQA evidence that semantic evidence preservation should be complemented by explicit 3D geometric diversity under aggressive budgets; moving this principle to object-level selection is cheap and fits the fixed-GT-box setting. IVSGround further narrows the novelty of question-conditioned view selection, making it even clearer that the unresolved thesis gap is not 'where to look' alone but how to preserve **unnamed supporting/context evidence** while aggressively reducing the object set rendered for open-ended ScanQA/SQA3D.
