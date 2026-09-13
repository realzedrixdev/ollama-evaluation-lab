# Ollama Evaluation Lab

**A reproducible, local-first benchmark laboratory for comparing offline language models.**

Ollama Evaluation Lab runs structured test suites against any Ollama models, stores every run in SQLite, scores deterministic and model-judged criteria, and generates standalone HTML leaderboards. It is designed to answer a practical question: *which local model is best for this language, task, and hardware budget?*

## Capabilities

- Benchmark multiple Ollama models from one experiment file
- Exact-match, contains, token-F1, latency, and JSON-validity metrics
- Kurdish, Arabic, and English test cases through UTF-8 JSONL datasets
- Warm-up requests and repeated trials
- Concurrent model execution with configurable workers
- Resumable SQLite run history and raw response audit trail
- Percentile latency and success-rate aggregation
- Weighted composite scoring with transparent formulas
- Self-contained HTML report with model cards and failure inspection
- Mock transport for fully deterministic tests

## Experiment lifecycle

```text
suite.jsonl + models
        ↓
experiment runner → Ollama /api/generate
        ↓                   ↓
raw responses          latency + errors
        └──────→ SQLite results
                         ↓
                  metrics engine
                         ↓
              HTML leaderboard/report
```

## Quick start

```bash
python -m model_lab run examples/kurdish_reasoning.jsonl --models llama3.2,qwen2.5 --db results.db
python -m model_lab report --db results.db --output report.html
python -m model_lab history --db results.db
python -m unittest discover -s tests
```

## Dataset format

Each JSONL row is independently auditable:

```json
{"id":"math-01","prompt":"What is 17 + 25?","expected":"42","metric":"exact","weight":1.0,"tags":["math","en"]}
```

Supported metrics are `exact`, `contains`, `token_f1`, and `valid_json`. Test cases may specify a system prompt, generation options, tags, and weight.

## Composite score

For each model, task scores are weight-averaged. Reliability is the successful-request fraction. The final score is:

```text
quality_score × reliability
```

Latency is reported separately (median and p95) so that quality and speed remain visible instead of being collapsed into an arbitrary number.

## Why local evaluation matters

Leaderboard results from large cloud models rarely predict edge deployment performance. Local evaluation captures the actual machine, quantization, language mix, prompt style, and latency constraints of a real project—especially important for Kurdish-language systems and privacy-sensitive deployments.

## License

MIT — built by [Karden Karwan](https://realzedrix.com).
