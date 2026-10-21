# Role-Aware Witness Coverage — 2026-10-21

Hypothesis: complete seed-answer-support bundles improve ScanQA/SQA3D at matched object budget.

Selector: retrieve named seeds with frozen semantics; search scene-wide for unnamed answer/support objects with soft relations; choose complete bundles before rendering. No exact-noun or KNN hard gate.

Test K=5/10/20, M=1/2. Metrics: CIDEr, EM, ORR, QEC, SCR (proxy without independent labels), witness recall, latency, VRAM. Risk: context loss high at K=5.

Scores /5: novelty 3.0, gain 3.7, feasibility 4.6, compute 4.8, fit 5.0, evidence 4.1.
