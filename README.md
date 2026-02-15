# MAC-Bench

MAC-Bench is a dynamic adversarial benchmark framework for evaluating **process compliance** in multi-agent systems under realistic pressure.

It implements a full SERV pipeline:

1. **Seed**: Parse policy text into machine-checkable atomic rules.
2. **Evolve**: Transform rules into pressure-injected adversarial scenarios.
3. **Refine**: Build auditable sandbox environments (DB, API, FS).
4. **Verify**: Run test-subject agents and audit complete trajectories.

## Key Features

- Process-centric compliance evaluation (not only task success).
- Dynamic scenario generation to reduce benchmark contamination.
- Social engineering pressure vectors (authority, urgency, empathy, obfuscation).
- Unified JSONL trajectory audit logs across all tools.
- Multiple auditor backends (deterministic, hybrid, llm-judge placeholder).
- Metrics: SR, CR, CSR, and Machiavelli Gap (MG).

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/run_benchmark.py --episodes 5
python scripts/analyze_results.py
```

Generated outputs:

- `data/atomic_rules/atomic_rules.json`
- `data/scenarios/scenarios.json`
- `data/sandbox_manifests/example.json`
- `results/episodes.jsonl`
- `results/violations.json`
- `results/metrics_summary.csv`

## Repository Layout

```text
mac-bench/
├── data/
├── agents/
├── sandbox/
├── evaluation/
├── prompts/
├── configs/
├── scripts/
└── results/
```

## Notes

- This repository ships with sample data and deterministic fallbacks to remain runnable offline.
- LLM integration points are intentionally abstracted so you can plug in your preferred provider.
