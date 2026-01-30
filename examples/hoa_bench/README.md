# HOA-Bench

Evaluation benchmark for HOA (Homeowners Association) management AI systems.

## Overview

Tests LLM ability to:
1. Apply HOA rules correctly (policy adherence)
2. Remain consistent across different resident framings
3. Resist manipulation attempts

## Structure

```
hoa_bench/
├── task.py            # Inspect AI task definitions
├── data/
│   └── scenarios/     # Evaluation scenarios (JSON)
└── rag/               # RAG infrastructure for CC&Rs
```

## Running

```bash
inspect eval examples/hoa_bench/task.py --model openai/gpt-4o
```
