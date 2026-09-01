# Thesis Research Shortlist

Project: 3D Scene Understanding with 2D Vision-Language Models via Abstract 3D Representations and Viewpoint Alignment

Last updated: 2026-09-01

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

## Evidence note: View-on-Graph (VoG), AAAI 2026
VoG is a peer-reviewed AAAI 2026 zero-shot 3D visual grounding method that externalizes spatial information into a multi-modal, multi-layer scene graph and lets a VLM selectively retrieve/traverse only necessary cues instead of processing the whole cluttered representation. This strengthens the evidence that selective structured retrieval is useful, but it also weakens novelty claims based only on 'scene graph + VLM + selective access'. No verified official GitHub repository was found in today's search.

Transfer implication: if a scene-graph variant is tested, use it as an ablation/baseline against OLT-QA rather than the thesis core. The thesis-specific gap should remain QA-specific supporting-context preservation + abstract-rendering evidence budget + PoseAlign-dependent relation refinement.

## Current top candidate
OLT-QA remains #1.

Reason: ViewMind3D and VoG make the novelty boundary clearer rather than replacing the top candidate. Generic question-conditioned view selection, language-guided grounding, structured reasoning, and selective graph traversal are now well-covered. The still-plausible gap is a lightweight QA-specific selector over fixed GT boxes that explicitly separates seed/referred objects from unnamed supporting/context objects, then renders only the retained pose-aligned abstract subscene and optimizes the QA-preservation vs object-retention trade-off.
