# Thesis Research Shortlist

Project: 3D Scene Understanding with 2D Vision-Language Models via Abstract 3D Representations and Viewpoint Alignment

Last updated: 2026-09-04

## Scope constraints
- Fixed ScanNet/ScanQA object annotations or 3D boxes as scene input.
- Detection/segmentation is not a thesis contribution.
- Prefer training-free / zero-shot / inference-only; 2D VLM <= ~7B where possible.
- Main pipeline: PoseRecover -> PoseAlign-T -> question-conditioned object/view selection -> 3D Abstract Renderer -> 2D VLM -> optional spatial verification / structured reasoning.
- Main object-selection method must not render the full scene.
- Seed/referred objects must be distinguished from unnamed supporting/context objects.

## Current weekly shortlist

### 1. OLT-QA: Question-conditioned Object Lookup + Geometry + Supporting-Context Expansion
Source inspiration: AgentGrounder (arXiv 2605.25901; ICRA 2026 MM-Spatial & SRRA Workshops; public code).

Hypothesis: With GT ScanNet instances replacing AgentGrounder's segmentation-built OLT, a lightweight query parser can retrieve seed/anchor objects, deterministic 3D geometry can resolve frame-safe relations, and a QA-specific support-expansion rule can preserve unnamed evidence before abstract rendering.

Transfer rule:
1. Build OLT from GT boxes: id, class, center, size, optional RGB/color summary.
2. Parse question into seed entities + relation + attribute cues.
3. Retrieve all plausible seed instances; avoid exact-noun-only matching.
4. Apply frame-safe geometry filters/ranking.
5. Expand supporting context using relation-conditioned neighbors, same-class distractors where needed, and short relation chains.
6. After PoseAlign-T, refine viewpoint-dependent left/right/front/behind relations.
7. Render only retained objects.

Primary risk: AgentGrounder is grounding, not QA; its retrieval logic does not establish which unnamed supporting objects ScanQA/SQA3D require.

Scores (1-5): Novelty 3.0; Expected Accuracy Gain 3.5; Feasibility 4.5; Compute Cost 4.0 (higher=cheaper); Fit 5.0; Evidence Strength 3.5.
Object-selection targets to test, not claims: Object Reduction Ratio 50-85%; Question Entity Coverage >=95% for explicit anchors; Supporting-Context Retention unknown; context-loss risk medium-high.

### 2. Object-Diversity Context Preservation inspired by 3DZip
Source: 3DZip, ECCV 2026, arXiv 2608.01185; public code.

Hypothesis: Pure semantic/KNN selection can collapse onto redundant objects; geometry-constrained diversity selection may retain more useful supporting evidence under a fixed object budget.

Transfer: after hard seed retention, represent each GT object with lightweight semantic + geometry features and select support objects using DPP/FPS-style diversity under spatial constraints. Do not adopt the LLaVA-3D token pipeline as the thesis core.

Scores: Novelty 3.5; Expected Accuracy Gain 3.0; Feasibility 3.5; Compute Cost 4.0; Fit 4.0; Evidence Strength 4.0.
Object-selection expectations: budget-controlled Object Reduction Ratio; Question Entity Coverage preserved via hard seed retention; Supporting-Context Retention potentially better than KNN; context-loss risk medium.

### 3. ViewMind3D-Guided Modular QA Baseline / Transfer
Source: ViewMind3D (arXiv 2607.28442, 2026-07-30; preprint; no verified official code as of this update).

Evidence: fully training-free; question-driven multi-view selection; language-conditioned grounding; BEV viewpoint indicator; structured reasoning; evaluated on ScanQA/SQA3D. Strongest setting uses OpenAI o3, so <=7B transfer requires separate validation.

Use: near-task baseline for view selection/structured reasoning; compare raw multi-view evidence against PoseRecover/PoseAlign-T + selected Abstract-3D subscene.

Scores: Novelty 2.0 standalone / 3.0 as transfer; Expected Accuracy Gain 4.0; Feasibility 3.0; Compute Cost 2.5; Fit 5.0; Evidence Strength 4.5.

### 4. Question-Aligned View Selection after Subscene Selection
Source: CoV, Findings of ACL 2026; training-free; evaluated on ScanQA/SQA3D.

Hypothesis: after compact subscene selection, question-aligned view selection/open-view refinement can improve visibility without many redundant views.

Use PoseAlign-T to initialize a canonical frame and apply view search only to the retained subscene. Treat as secondary module/ablation because generic question-conditioned view selection is already well covered.

Scores: Novelty 2.5; Expected Accuracy Gain 4.0; Feasibility 3.5; Compute Cost 3.0; Fit 4.5; Evidence Strength 5.0.

### 5. TDVR-inspired Structured Query + Distractor-aware Pose Refinement
Source: TDVR (arXiv 2608.03763, 2026-08-04; preprint; no verified official code as of this update).

Hypothesis: structured target/anchor/attribute/relation parsing can improve seed-instance resolution; post-PoseAlign distractor filtering can reduce same-class clutter.

Supporting-context rule: never discard non-seed neighbors merely for low semantic similarity; this module only resolves seed ambiguity, while QA support expansion remains separate.

Scores: Novelty 2.5; Expected Accuracy Gain 3.5; Feasibility 4.0; Compute Cost 4.0; Fit 4.5; Evidence Strength 3.5.
Object-selection expectations: medium Object Reduction Ratio; improved Question Entity Coverage under same-class ambiguity; Supporting-Context Retention neutral unless combined with OLT-QA; context-loss risk medium if pruning is aggressive.

### 6. Post-selection Geometry-Aware Visual Token Pruning
Source: Seeing Once is Enough? Online Geometry-Aware Token Pruning for 3D Question Answering (arXiv 2607.04079; First Workshop on Efficient Spatial Reasoning at ICLR 2026; no verified public code yet).

Evidence: training-free and directly tested with Qwen2.5-VL-7B/Qwen3-VL-8B on ScanQA/SQA3D/OpenEQA-HM3D. It projects posed RGB-D observations to a shared voxel space and prunes visual tokens corresponding to already-observed geometry. Reported up to ~50% token reduction. With Qwen2.5-VL-7B online uniform sampling, ScanQA EM 24.1 -> 25.1 and CIDEr 65.6 -> 69.3 while tokens fall 37.1M -> 32.6M; SQA3D EM 46.5 -> 47.3 while tokens fall 28.0M -> 24.1M.

Research Hypothesis: after OLT-QA + PoseAlign-T + abstract multi-view rendering, geometry-aware redundancy pruning can reduce cross-view tokens without deleting selected seed/support objects.

Object-selection rule: unchanged; OLT-QA runs first.
Supporting-context rule: protect all selected seed/support objects at object level; prune only redundant visual patches represented elsewhere in the retained views.
Expected benefit: lower token/VRAM/latency and possibly less attention dilution.
Difficulty: medium; requires depth/pose projection and access to the VLM visual-token path.
Compute: no training; demonstrated directly with a 7B VLM. Exact VRAM not reported.
Metrics: ScanQA/SQA3D QA metrics, visual-token count, latency, peak VRAM, plus upstream Object Reduction Ratio/Question Entity Coverage/Supporting-Context Retention.
Ablations: selected subscene only; + view selection; + token pruning; + both; pruning threshold sweep; protected-object mask on/off.
Risk: does not solve relevant-object selection; cannot be thesis novelty by itself.
Scores: Novelty 2.0 standalone / 2.5 integration; Expected Accuracy Gain 3.0; Feasibility 4.0; Compute Cost 4.5; Fit 4.0; Evidence Strength 4.5.

## Evidence notes

### GuideGround (arXiv 2608.00518)
Preserves per-view grounding hypotheses and verifies them separately before aggregation. Transfer only as a multi-view verification ablation after compact subscene selection; not thesis novelty.

### View-on-Graph, AAAI 2026
Zero-shot 3D grounding through selective reasoning over a multi-modal scene graph. This weakens novelty claims based only on `scene graph + VLM + selective access`; use as baseline/ablation, not core contribution.

### SpatialPrompting, Frontiers in Robotics and AI 2026
Peer-reviewed, training-free pose-aware keyframe selection; evaluates ScanQA/SQA3D and includes Qwen2.5-VL-7B experiments. Strong baseline for view selection but not novelty.

### UniGround, arXiv 2603.08131
Training-free global candidate filtering + local precision grounding. Strong evidence for semantic candidate filtering, but it solves referred-target grounding rather than unnamed QA supporting-context retention.

### SmartMage, arXiv 2608.05137
Query-adaptive modality routing for 3D scene understanding. Relevant evidence that query-dependent evidence selection matters, but it is a trained unified MLLM rather than a training-free object/subscene selector; not a direct candidate.

## Current top candidate
**OLT-QA remains #1.**

Reason: the new geometry-aware pruning evidence improves efficiency after multi-view rendering but does not solve the unresolved QA-specific problem: identify explicit seed/referred objects while preserving unnamed supporting/context objects, then reduce the Abstract-3D subscene aggressively without sacrificing answerability. The core evaluation should remain QA preservation vs Object Reduction Ratio, with explicit Question Entity Coverage and Supporting-Context Retention analysis.
