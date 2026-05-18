# SensitivityOS

An open-source, graph-powered data sensitivity classification framework.

## Core Innovations

- Semantic sensitivity graph traversal — contextual escalation across related fields
- Community classifier registry — YAML-driven, Git-versioned, domain-specific rules
- Explainable uncertainty — reviewers see exactly which graph edges fired
- Self-improving feedback loop — reviewer corrections written back as new graph edges
- 100 % local stack — no cloud APIs, no vendor lock-in

## Quickstart

### Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com/) installed and running with `phi3` pulled:
  ```bash
  ollama pull phi3
  ```
- spaCy English model:
  ```bash
  python -m spacy download en_core_web_lg
  ```

### Install & run

```bash
# From the project root
cd backend
pip install -r requirements.txt

# Launch the API + frontend (served at http://127.0.0.1:8000)
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000` in your browser.

### Classify via the dashboard

1. Click **Upload & Analyse** and select a CSV file (samples in `datasets/`).
2. View the **Final Classifications**, **Semantic Sensitivity Graph**, and **Explainability Explorer**.
3. Items below the 75 % confidence threshold appear in the **Human Review Queue** — submit corrections to feed back into the graph.

### Classify via the API

```bash
# Upload a CSV directly
curl -F "file=@datasets/sample_healthcare_data.csv" http://127.0.0.1:8000/upload

# Or classify a local path
curl "http://127.0.0.1:8000/classify?path=$(pwd)/datasets/sample_hr_data.csv"
```

### Run tests

```bash
# From backend/
python test_graph.py
python test_pipeline.py
```

## Tech Stack (100 % free & open-source)

| Component | Technology |
|---|---|
| PII entity recognition | Microsoft Presidio + spaCy |
| Knowledge graph engine | NetworkX |
| Data scanning | DuckDB |
| Local LLM inference | Ollama + Phi-3 |
| Backend API | FastAPI |
| Frontend | Vanilla JS + Chart.js + vis-network |
| Classifier registry | YAML + Git |
| License | Apache 2.0 |

## Registry

Community classifiers live in `registry/`. Add a new `.yaml` or `.yml` file following the schema in `registry/REGISTRY_SPEC.md` and it is picked up automatically on next server start.
