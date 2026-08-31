# Thesis Research Shortlist

Project: 3D Scene Understanding with 2D Vision-Language Models via Abstract 3D Representations and Viewpoint Alignment

Last updated: 2026-08-31

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

### 3. Question-Aligned View Selection after Subscene Selection
Source inspiration: CoV, Findings of ACL 2026; public code; training-free; evaluated on ScanQA/SQA3D.

Hypothesis: Once a compact object subscene is available, question-aligned view selection/open-view refinement can improve evidence visibility without rendering many redundant views.

Transfer rule: run selection on the retained subscene, not full scene; use PoseAlign-T to initialize canonical view, then select/adjust a small number of views based on question evidence.

Scores: Novelty 2.5 as a standalone contribution; Expected Accuracy Gain 4.0; Feasibility 3.5; Compute Cost 3.0; Fit 4.5; Evidence Strength 5.0.
Risk: view-search cost and overlap with existing CoV; should be secondary module/ablation, not main novelty.

## Current top candidate
OLT-QA (AgentGrounder-inspired online retrieval, but using GT boxes and adding QA-specific supporting-context expansion + post-PoseAlign relation refinement).

Reason: it is the closest published/open implementation to the exact operational need: retrieve only relevant object candidates from an object table, use deterministic geometry, and render visual evidence on demand. The thesis-specific gap is not the OLT itself; it is adapting this grounding pipeline to QA, preserving unnamed supporting context, and integrating viewpoint-dependent refinement with PoseAlign-T while keeping the backbone small.
