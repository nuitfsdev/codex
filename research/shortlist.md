# Thesis Research Shortlist

Project: 3D Scene Understanding with 2D Vision-Language Models via Abstract 3D Representations and Viewpoint Alignment

Last updated: 2026-09-09

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
Primary evidence: GraFT (arXiv:2609.03892), **PruneGround (arXiv:2606.31148)**, SceneGraphGrounder (arXiv:2605.21788), ObsGraph (arXiv:2606.24068), and SeGPruner (arXiv:2603.29437).

**Novelty boundary:** GraFT already performs training-free selective rendering/retrieval of referenced/query-relevant objects. SceneGraphGrounder already parses query graphs and performs relation-aware constrained graph matching. SeGPruner already provides direct ScanQA evidence for semantic saliency + explicit 3D geometric diversity under aggressive token budgets. Most importantly, PruneGround's public implementation explicitly introduces `anchors_visual`: anchors detected in side views but absent from the original referring expression. Therefore **generic discovery/expansion of unnamed visual objects is no longer a defensible novelty claim**.

The remaining defensible gap is narrower: **QA-utility-aware unnamed support selection under a strict object/render budget**. PruneGround uses visually inferred anchors to improve target grounding; it does not optimize a minimal support set for open-ended ScanQA/SQA3D answer evidence, report QA-vs-object-budget trade-offs, or isolate the causal utility of unnamed support objects.

**Research Hypothesis:** open-ended ScanQA/SQA3D questions can require unnamed supporting/context objects beyond referred entities. A support selector that optimizes downstream QA utility using relation compatibility, optional co-visibility, and explicit geometric diversity under a fixed object budget can preserve a minimal useful subscene better than seed-only or grounding-oriented pruning; PoseAlign-T then refines viewpoint-dependent relations before Abstract-3D rendering.

**Current transfer rule:**
1. Build object table from fixed GT boxes: id, class, center, extent, optional RGB summary.
2. Parse explicit seed entities/attributes/relation intent; resolve plausible seed instances with synonyms/frozen semantics. Hard-retain seeds and delay ambiguous same-class pruning.
3. Generate unnamed support candidates from cheap box relations: near, above/below, support/contact, containment, overlap, functional/spatial cluster.
4. Optionally add a co-visibility prior from existing camera metadata; this must not require rendering the full scene as the main method.
5. Under a fixed object budget, allocate support slots between high relation/semantic evidence and spatially diverse context.
6. After PoseAlign-T, recompute viewpoint-dependent left/right/front/behind relations and prune incompatible supports.
7. Render only retained seed+support objects.

**Evaluation:** ScanQA/SQA3D downstream QA; Object Reduction Ratio; Question Entity Coverage; object-budget-vs-QA curve; Context Benefit Rate (`Seed+Support correct && Seed-only wrong`); Support Ablation Sensitivity. Supporting-Context Retention remains proxy-only unless explicit support-object GT is introduced.

**Core matched-budget ablation:** Full Scene vs GraFT-style Seed-only vs SceneGraphGrounder-style query-graph nodes vs **PruneGround-inspired visual-anchor expansion** vs Seed+KNN vs Seed+radius vs Seed+relation-aware support vs Seed+co-visibility vs Seed+spatial-diversity vs Seed+relation+co-visibility+diversity vs +PoseAlign-T.

**Scores (1-5):** Novelty **3.4**; Expected Accuracy Gain 3.6; Feasibility 4.6; Compute Cost 4.7 (higher=cheaper); Fit 5.0; Evidence Strength **4.8**.
**Targets to test, not claims:** Object Reduction Ratio 50-85%; Question Entity Coverage >=95%; Supporting-Context Retention unknown/proxy-only; context-loss risk medium.
**Publication potential:** moderate only if matched-budget experiments show that QA-specific support selection preserves/gains answer accuracy beyond grounding-oriented visual-anchor discovery. If not, this becomes an adaptation rather than a strong contribution.

### 2. QASER: QA-Specific Evidence Retention
Source inspiration: PruneGround's LGSP/MCDR and public `anchors_visual` schema, combined with GraFT/SeGPruner.

**Role:** strongest current refinement of SAFER-QA. Candidate utility is defined by downstream QA preservation/gain rather than grounding-anchor usefulness. Hard-retain seeds, expand unnamed support with relation geometry, then allocate a strict budget with diversity/co-visibility priors before PoseAlign-T and rendering.

**Important constraint:** only PruneGround's pruning/reformulation ideas transfer cleanly. Its full LLM-Grounder is not training-free; it repurposes/fine-tunes a detection-pretrained spatial LLM. Default public pruning/reformulation model is Qwen2.5-VL-3B-Instruct, which fits the preferred model-size envelope.

**Scores:** Novelty 3.4; Expected Accuracy Gain 3.6; Feasibility 4.6; Compute Cost 4.7; Fit 5.0; Evidence Strength 4.8.

### 3. RCSX: Relation-Conditioned Supporting-Object Expansion
Sources: ReasoningGraph (ICRA 2026), View-on-Graph (AAAI 2026), SceneGraphGrounder (2026 preprint).

Role: symbolic support generator inside SAFER-QA/QASER. Query-graph relation matching is already prior art. Differentiation must be expansion beyond referred/query-graph nodes to unnamed QA evidence, under a strict rendering budget, followed by PoseAlign-T refinement.

Scores: Novelty 2.5 standalone / 3.3 inside SAFER-QA; Expected Accuracy Gain 3.5; Feasibility 4.5; Compute Cost 4.5; Fit 5.0; Evidence Strength 4.5.

### 4. OLEA: Object-Level Evidence Allocation inspired by SeGPruner
Source: SeGPruner (arXiv:2603.29437; public code `intcomp/SegPruner`).

Hypothesis: move SeGPruner's saliency-plus-geometric-diversity principle one level earlier, from visual-token pruning to GT-object budget allocation. Hard-retain seeds, rank relation/semantic supports, reserve budget for spatially diverse context, then PoseAlign-T prune viewpoint-incompatible candidates before rendering.

Role: budget allocator inside SAFER-QA/QASER, not standalone novelty.

Scores: Novelty 3.0 standalone / 3.5 integration; Expected Accuracy Gain 3.5; Feasibility 4.7; Compute Cost 4.8; Fit 5.0; Evidence Strength 4.6.

### 5. CoVis-Support: Co-visibility/Evidence-Preserving Support Expansion
Source inspiration: ObsGraph (arXiv:2606.24068; under review).

Hypothesis: objects repeatedly co-visible with grounded seeds in informative views provide a training-free contextual prior complementary to geometry relations. Use only as a prior/tie-breaker; avoid any implementation that requires full-scene rendering in the main method.

Risks: incidental clutter, camera-coverage bias, large/frequent-object bias.

Scores: Novelty 2.8 standalone / 3.3 integration; Expected Accuracy Gain 3.5; Feasibility 4.5; Compute Cost 4.5; Fit 5.0; Evidence Strength 3.5.

### 6. OLT-QA Seed Retrieval Front End
Sources: AgentGrounder, GraFT, PruneGround.

Role: baseline/front end only. Build a lightweight object table from GT boxes and use question parsing + synonyms/frozen semantics to identify seed/referred objects. Do not claim generic lookup, relevant-class extraction, referred-object selection, or local-region pruning as novelty.

Scores: Novelty 1.3 standalone / 2.2 as component; Expected Accuracy Gain 3.0; Feasibility 4.5; Compute Cost 4.5; Fit 4.5; Evidence Strength 4.7.

### 7. Object-Diversity Context Preservation inspired by 3DZip
Source: 3DZip, ECCV 2026, arXiv:2608.01185; public code.

Use only as a support-budget tie-breaker after hard seed retention and support expansion; choose diverse supports rather than redundant nearest neighbors. SeGPruner supplies more direct ScanQA evidence for the same high-level principle.

Scores: Novelty 2.5 integration; Expected Accuracy Gain 3.0; Feasibility 3.5; Compute Cost 4.0; Fit 4.0; Evidence Strength 4.2.

### 8. Question-Aligned View Selection after Subscene Selection
Sources: CoV (Findings ACL 2026), SpatialPrompting (Frontiers 2026), GraFT, ViewMind3D, IVSGround, PruneGround MCDR.

Strong precedent exists. Treat view selection as secondary module/ablation: after support selection and PoseAlign-T, choose the smallest views jointly exposing retained seeds/supports. Do not claim question-conditioned view selection itself as novelty.

Scores: Novelty 1.6; Expected Accuracy Gain 4.0; Feasibility 4.0 for training-free heuristic; Compute Cost 3.5; Fit 4.5; Evidence Strength 5.0.

### 9. Post-selection Geometry-Aware Visual Token Pruning
Sources: Seeing Once is Enough? (arXiv:2607.04079; ICLR 2026 workshop), SeGPruner.

Role: efficiency ablation after selected-subscene multi-view rendering. Protect selected seed/support objects at object level and prune only redundant cross-view patches/tokens.

Scores: Novelty 1.8 standalone / 2.3 integration; Expected Accuracy Gain 3.0; Feasibility 4.0; Compute Cost 4.5; Fit 4.2; Evidence Strength 4.8.

## Evidence notes retained
- **PruneGround (2026-06-30):** arXiv/CoRR preprint; public MIT code. LGSP uses frozen VLM spatial pruning; MCDR reforms target-anchor relations and public outputs include `anchors_visual` absent from the original description. Default VLM is Qwen2.5-VL-3B-Instruct. Reported pruning target recall ~94.7%; candidates drop 5.72->1.62 on ScanRefer Multiple and 2.43->1.28 on Sr3D Hard. Strong novelty limiter for any generic unnamed-object-expansion claim. Full LLM-Grounder is not training-free.
- **GraFT (2026-09-03):** training-free 3DSG; GT ScanNet-compatible setting; query-relevant selective BEV; geometry-guided egocentric frame retrieval; Qwen2.5-VL-7B on ScanQA. Core near-task baseline.
- **SeGPruner (2026-03-31):** training-free semantic+geometry token pruning; ScanQA/OpenEQA; public code; LLaVA-OneVision-Qwen2-7B. Strong evidence for dual evidence allocation, but at token rather than object level.
- **SceneGraphGrounder (2026-05-20):** zero-shot query graph + semantic filtering + constrained relation graph matching; ScanRefer; preprint. Important novelty limiter for RCSX.
- **ObsGraph (2026-06-23):** room-view-object hierarchy, bounded retrieval, co-visibility/raw-evidence preservation; not ScanQA-specific.
- **ViewMind3D:** training-free question-driven multi-view selection + grounding + BEV + structured reasoning on ScanQA/SQA3D; strongest setup uses proprietary large models.
- **UniGround / TDVR / AgentGrounder:** strong precedents for seed candidate filtering, structured target-anchor-relation parsing, geometric scoring, and selective object retrieval; not sufficient novelty by themselves.

## Current top candidate
**SAFER-QA / QASER refinement: QA-utility-aware unnamed support selection for selective Abstract-3D rendering.**

Best current instantiation:
`seed retrieval -> relation-aware unnamed support candidates -> optional co-visibility prior -> fixed-budget semantic/relation + spatial-diversity allocation -> PoseAlign-T directional refinement -> selective Abstract-3D render -> <=7B VLM`.

Reason: PruneGround materially narrows the novelty gap by already discovering visual anchors that are absent from language. Therefore the proposal should no longer claim that 'support objects need not be named' is itself new. The stronger and still testable thesis claim is that **objects useful for open-ended QA are not the same as objects useful as grounding anchors**, and that a QA-specific budgeted selector can preserve answer evidence better than seed-only or grounding-oriented pruning at the same render budget.
