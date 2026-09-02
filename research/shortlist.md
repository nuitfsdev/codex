# Thesis Research Shortlist

Project: 3D Scene Understanding with 2D Vision-Language Models via Abstract 3D Representations and Viewpoint Alignment

Last updated: 2026-09-02

## Scope constraints
- Fixed ScanNet/ScanQA object annotations or 3D boxes as scene input.
- Detection/segmentation is not a thesis contribution.
- Prefer training-free / zero-shot / inference-only; 2D VLM <= ~7B where possible.
- Main pipeline: PoseRecover -> PoseAlign-T -> question-conditioned object/view selection -> 3D Abstract Renderer -> 2D VLM -> optional spatial verification / structured reasoning.
- Object-selection track must avoid rendering the full scene as the main method.

## Current weekly shortlist

### 1. OLT-QA: Question-conditioned Object Lookup + Geometry + Supporting-Context Expansion
Source inspiration: AgentGrounder (arXiv 2605.25901; ICRA 2026 MM-Spatial & SRRA Workshops; public code).

Hypothesis: With GT ScanNet instances replacing AgentGrounder's Mask3D OLT, a lightweight query parser can retrieve seed/anchor object categories, deterministic 3D geometry can resolve spatial candidates, and a context-expansion rule can preserve unnamed supporting objects before abstract rendering.

Transfer rule:
1. Build Object Lookup Table directly from GT boxes: id, class, center, size, optional RGB/color summary.
2. Parse question into seed entities + relations + attribute cues.
3. Retrieve all candidate instances for seed categories; never exact-noun-only if an answer category is implicit.
4. Apply relation-specific geometric filtering/ranking where relation is frame-safe.
5. Expand with supporting context: spatial neighbors / same-class distractors / relation-chain candidates.
6. After PoseAlign-T, refine viewpoint-dependent left/right/front/behind relations.
7. Render only retained objects.

Primary risk: AgentGrounder is a 3D visual grounding method evaluated on ScanRefer/Nr3D, not QA. Its original online agent uses a much larger VLM than the thesis target, so the transfer to <=7B must be validated.

Scores (1-5): Novelty 3.0; Expected Accuracy Gain 3.5; Feasibility 4.5; Compute Cost 4.0 (higher=cheaper); Fit 5.0; Evidence Strength 3.5.
Object-selection expectations to test, not claims: Object Reduction Ratio 50-85%; Question Entity Coverage >=95% for explicit anchors; Supporting-Context Retention unknown and must be measured via ablation; context-loss risk medium-high.

### 2. Object-Diversity Context Preservation inspired by 3DZip
Source inspiration: 3DZip, ECCV 2026, arXiv 2608.01185; public code.

Hypothesis: Semantic/question-conditioned selection tends to collapse onto only directly mentioned objects; adding a geometry-constrained diversity objective at object level can preserve spatially distinct supporting evidence with a fixed object budget.

Transfer rule: after seed retrieval, represent each GT object by lightweight semantic + geometry features; choose supporting objects using diversity-aware selection (e.g. DPP/FPS-style) under spatial constraints instead of pure KNN. Do not adopt LLaVA-3D token pipeline.

Primary risk: 3DZip proves token compression, not question-conditioned object selection; object-level transfer is a new hypothesis and may retain irrelevant diversity.

Scores: Novelty 3.5; Expected Accuracy Gain 3.0; Feasibility 3.5; Compute Cost 4.0; Fit 4.0; Evidence Strength 4.0.
Object-selection expectations: Object Reduction Ratio budget-controlled; Question Entity Coverage determined by hard seed retention; Supporting-Context Retention potentially better than KNN; context-loss risk medium.

### 3. ViewMind3D-Guided Modular QA Baseline / Transfer
Source: ViewMind3D: Modular View-Aware Inference for Training-Free 3D-QA (arXiv 2607.28442, 2026-07-30; preprint; no verified official code found as of 2026-09-01).

Evidence: fully training-free; question-driven multi-view selection; guided visual grounding with language-conditioned object cues; BEV viewpoint indicator; role-based structured reasoning; evaluated directly on ScanQA/SQA3D. Reported 73.4 CIDEr on ScanQA and 50.8% overall accuracy on SQA3D. Strongest reported setting uses OpenAI o3, so it does not satisfy the <=7B local-backbone constraint directly.

Candidate hypothesis: replace ViewMind3D's generic multi-view evidence stage with PoseRecover/PoseAlign-T + compact Abstract-3D subscene evidence. Use ViewMind3D mainly as a near-task baseline for question-driven view selection, grounding, and structured reasoning.

Stage changed: view/evidence selection and final structured reasoning.
Object-selection rule: not a standalone object selector; use it only after OLT-QA/subscene selection or as a baseline that selects views from the full scene.
Supporting-context rule: preserve context through selected views; compare against explicit object-level support expansion.
Expected benefit: validates whether abstract pose-aligned evidence can outperform/reduce the cost of raw multi-view observations.
Difficulty: medium. Compute: potentially high in the published strongest setting due to o3/API inference; local <=7B transfer must be separately benchmarked.
Ablation: full-scene multi-view vs selected-subscene abstract views; with/without BEV indicator; with/without structured answer roles.
Risk: overlap is high for generic question-conditioned view selection; this must not be claimed as novelty.
Scores: Novelty 2.0 standalone / 3.0 as transfer; Expected Accuracy Gain 4.0; Feasibility 3.0; Compute Cost 2.5; Fit 5.0; Evidence Strength 4.5.

### 4. Question-Aligned View Selection after Subscene Selection
Source inspiration: CoV, Findings of ACL 2026; public code; training-free; evaluated on ScanQA/SQA3D.

Hypothesis: Once a compact object subscene is available, question-aligned view selection/open-view refinement can improve evidence visibility without rendering many redundant views.

Transfer rule: run selection on the retained subscene, not full scene; use PoseAlign-T to initialize canonical view, then select/adjust a small number of views based on question evidence.

Scores: Novelty 2.5 as a standalone contribution; Expected Accuracy Gain 4.0; Feasibility 3.5; Compute Cost 3.0; Fit 4.5; Evidence Strength 5.0.
Risk: view-search cost and overlap with existing CoV; should be secondary module/ablation, not main novelty.

### 5. TDVR-inspired Structured Query + Distractor-aware Pose Refinement
Source: TDVR: Joint Text Disambiguation and Viewpoint Reasoning for Zero-Shot 3D Visual Grounding (arXiv 2608.03763, 2026-08-04; preprint; no verified official code found as of 2026-09-02).

Evidence: TDVR is training-free. It builds a semantic 3D scene graph, enriches/disambiguates the query with appearance and spatial descriptions, infers an optimal viewpoint, explicitly scores confusion among similar instances, and combines viewpoint/category/appearance evidence. It reports strong zero-shot gains on ScanRefer and 70.0% overall / 79.03% viewpoint-dependent accuracy on Sr3D. It is grounding, not QA, and its scene-graph construction should not be copied as the thesis core.

Research Hypothesis: For ScanQA/SQA3D, a lightweight structured query representation can improve seed-instance resolution before supporting-context expansion, while a distractor-aware score after PoseAlign-T can prevent same-class objects from polluting a compact abstract subscene.

Stage changed: question parsing + seed-object resolution + post-PoseAlign distractor pruning.
Object-selection rule: parse target/anchor/attribute/relation cues; retain all plausible same-category seed instances initially; after PoseAlign-T, rank or remove same-class distractors using frame-aligned geometry plus optional object-crop semantic similarity.
Supporting-context rule: never prune non-seed neighbors solely because they have low category similarity; support expansion remains relation-conditioned and is evaluated separately from seed disambiguation.
Expected benefit: higher Question Entity Coverage under instance ambiguity and lower object count after pose-aware disambiguation, without exact noun-only selection.
Implementation difficulty: medium.
Data/metrics: ScanQA/SQA3D QA metrics; object retention; seed-entity coverage where measurable; same-class distractor count before/after; downstream QA preservation.
Compute estimate: no task-specific training; geometry is negligible; CLIP/SigLIP crop scoring is lightweight. A <=7B local parser/VLM should fit roughly 12-20 GB VRAM depending on quantization/context, but this is an implementation estimate, not a paper-reported requirement.
Ablations: raw noun seeds vs structured query; keep-all same-class vs distractor-aware refinement; refinement before vs after PoseAlign-T; geometry-only vs geometry+appearance.
Risks: TDVR already covers structured query disambiguation + viewpoint-aware distractor discrimination, so copying this stack has low novelty. The thesis-specific value would need to come from QA supporting-context retention and abstract-rendering budget, not the disambiguation mechanism itself.
Publication potential: moderate only as a supporting module; weak as standalone novelty.
Scores: Novelty 2.5; Expected Accuracy Gain 3.5; Feasibility 4.0; Compute Cost 4.0; Fit 4.5; Evidence Strength 3.5.
Object-selection expectations: Object Reduction Ratio medium; Question Entity Coverage potentially improved for ambiguous same-class scenes; Supporting-Context Retention neutral unless combined with OLT-QA support expansion; context-loss risk medium if distractor pruning is aggressive.

## Evidence note: GuideGround (arXiv 2608.00518)
GuideGround preserves per-view grounding hypotheses and explicitly verifies them with a VLM instead of indiscriminately aggregating multi-view features. It is not training-free end-to-end in the same sense as the thesis target because it complements task-specific grounding models, and it is evaluated on ReferIt3D rather than ScanQA/SQA3D. The transferable lesson is narrow: after compact subscene selection, keep per-view hypotheses separate and verify consistency before multi-view aggregation. Treat this as an ablation/verification module, not novelty.

## Evidence note: View-on-Graph (VoG), AAAI 2026
VoG is a peer-reviewed AAAI 2026 zero-shot 3D visual grounding method that externalizes spatial information into a multi-modal, multi-layer scene graph and lets a VLM selectively retrieve/traverse only necessary cues instead of processing the whole cluttered representation. This strengthens the evidence that selective structured retrieval is useful, but it also weakens novelty claims based only on 'scene graph + VLM + selective access'. No verified official GitHub repository was found in today's search.

Transfer implication: if a scene-graph variant is tested, use it as an ablation/baseline against OLT-QA rather than the thesis core. The thesis-specific gap should remain QA-specific supporting-context preservation + abstract-rendering evidence budget + PoseAlign-dependent relation refinement.

## Current top candidate
OLT-QA remains #1.

Reason: TDVR strengthens the case for structured seed disambiguation and pose-aware distractor filtering, but it also removes those mechanisms from the novelty space. OLT-QA remains ahead because its unresolved question is QA-specific: how to preserve unnamed supporting/context objects while aggressively reducing the rendered abstract subscene. Generic question-conditioned view selection, language-guided grounding, structured reasoning, and selective graph traversal are already well-covered.
