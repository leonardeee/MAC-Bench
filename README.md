# MAC-Bench (Multi-Agent Compliance Benchmark)

This repository contains the core implementation of **MAC-Bench**, an automated multi-agent compliance benchmark system built around the **Agent-as-a-Benchmark** workflow. It generates compliance seeds, adversarial scenarios, runnable sandbox environments, and executes evaluations end-to-end.

## Project Structure

```text
mac-bench/
├── assets/                  # Raw rule documents (PDF/TXT)
├── config/                  # Config files (API Keys, Docker config)
├── data/
│   ├── seeds/               # Extracted atomic rules (JSON)
│   ├── scenarios/           # Generated scenarios (JSON)
│   └── traces/              # Execution traces/logs
├── src/
│   ├── generator/           # Generation-side agents
│   │   ├── rule_parser.py   # Rule extraction
│   │   ├── architect.py     # Scenario writer (red team)
│   │   └── builder.py       # World Builder
│   ├── simulation/          # Execution modules
│   │   ├── sandbox.py       # Docker sandbox manager
│   ├── evaluation/          # Evaluation modules
│   │   └── judge.py         # Auto scorer
│   ├── utils/               # Utilities
│   └── main.py              # Entry point
├── templates/               # Dockerfile and prompt templates
├── requirements.txt
└── README.md
```

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/main.py
```

## Notes

- Make sure Docker is running for sandbox execution.
- You will need an OpenAI-compatible API key for the generator modules.
