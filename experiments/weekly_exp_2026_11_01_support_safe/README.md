# Weekly Thesis Experiment — 2026-11-01 (W44)

Winner: **SAFER-QA / QASER-PreRender — Support-Safe Relational Witness Budget**.

Research status: **INCONCLUSIVE** (ScanQA/SQA3D QA benchmark not run).

## CPU diagnostics (not ScanQA results)
- 26/26 unit tests PASS; 500/500 metamorphic checks PASS.
- 30 manually constructed toy variants (six families x five jitter variants), seed 20261101.
- A Full: 10.83 objects, ORR 0%, toy support recall 100%.
- B Seed: 1.00 objects, ORR 90.52%, toy support recall 0%.
- C Nearest K6: 6.00 objects, ORR 43.13%, toy support recall 93.75%.
- C matched to D: 3.67 objects, ORR 67.24%, toy support recall 60.42%.
- D Proposed: 3.67 objects, ORR 67.24%, toy support recall 75.42%.
- E Toy oracle: 3.83 objects, ORR 67.05%, toy support recall 100%.

D exceeds C-matched by 15.00pp **toy proxy** recall, but is below C K6 by 18.33pp. No QA/accuracy gain is claimed. One two-hop example misses the true bridge despite status OK; five missing-frame and five count-overbudget cases correctly flag incompleteness.

## Evaluation protocol

A Full / B Seed / C Nearest / D Role-preserving subscene, plus frozen BGE-small/MiniLM semantic Top-K and optional Oracle. Main method renders **selected objects only**. Real acceptance: >=50% ORR with <=1pp QA loss vs full scene, or QA gain with positive reduction. Match object count, view count, renderer, prompt, VLM, decoding, seed. Use ScanQA EM@1/CIDEr/ROUGE-L, SQA3D Accuracy/EM and latency/token metrics.

## Blockers

No licensed ScanNet boxes/meshes, verified PoseAlign outputs, instance-mesh renderer, frozen <=7B VLM GPU backend, independent seed grounding or complete supporting-object GT in the execution environment. No training, GPU benchmark, or external cost was incurred.

The full runnable CPU reference implementation, tests, JSON adapter, toy logs, results, and detailed report were produced as a downloadable conversation artifact named `weekly_thesis_experiment_2026-11-01.zip`. **This repository entry is a research record, not a claim that those files have been committed.**
