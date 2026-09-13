# Weekly Thesis Experiment 004

## Winning Candidate
**Adaptive Relation-Chain Subscene Selection**

## Research Hypothesis
A training-free selector that expands from seed objects along question-implied relation hops can remove at least 50% of scene objects while retaining answer-critical bridge/support objects much better than seed-only or KNN pruning.

## Setup
- Seed: 42
- Synthetic scenes: 20,000
- Objects per scene: 24
- Two-hop probability: 45%
- Relations: left/right/front/behind/near
- A: full scene
- B: seed only
- C: seed + four nearest objects
- D: adaptive relation-chain expansion (beam=3)
- E: oracle required nodes
- No training; CPU only.

## Actual Results
| Method | Avg objects | Reduction | Support recall | Full required retention | 1-hop retention | 2-hop retention |
|---|---:|---:|---:|---:|---:|---:|
| A Full | 24.00 | 0.00% | 100.00% | 100.00% | 100.00% | 100.00% |
| B Seed | 1.00 | 95.83% | 0.00% | 0.00% | 0.00% | 0.00% |
| C KNN | 5.00 | 79.17% | 50.86% | 42.71% | 56.05% | 26.62% |
| D Adaptive | 8.08 | 66.34% | 95.93% | 95.45% | 93.69% | 97.56% |
| E Oracle | 2.45 | 89.78% | 100.00% | 100.00% | 100.00% | 100.00% |

Sanity acceptance: PASS. Unit tests: 3/3 passed. CPU experiment runtime: 1.095 s.

## Beam Ablation
- beam=1: 2.45 objects, 89.79% reduction, 56.60% support recall
- beam=2: 4.80 objects, 80.01% reduction, 83.25% support recall
- beam=3: 8.04 objects, 66.48% reduction, 95.73% support recall
- beam=4: 12.19 objects, 49.21% reduction, 97.91% support recall

## Interpretation
KNN strongly truncates multi-hop support chains: only 26.62% complete two-hop retention. The relation-chain selector retains 97.56% while removing 66.34% of objects. These are synthetic selector diagnostics, not ScanQA/SQA3D QA scores.

## Status
Synthetic mechanism: SUPPORT_SANITY_ONLY. Overall thesis hypothesis: INCONCLUSIVE. Real ScanQA/SQA3D VLM benchmark remains BLOCKED until ScanNet assets/object boxes and GPU inference backend are available.
