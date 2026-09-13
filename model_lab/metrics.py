import json
import re
from collections import Counter


def normalized(value: object) -> str:
    return re.sub(r"\s+", " ", str(value).strip().casefold())


def token_f1(actual: str, expected: str) -> float:
    a, e = Counter(normalized(actual).split()), Counter(normalized(expected).split())
    overlap = sum((a & e).values())
    if not a or not e: return float(a == e)
    precision, recall = overlap / sum(a.values()), overlap / sum(e.values())
    return 2 * precision * recall / (precision + recall) if precision + recall else 0.0


def score(metric: str, actual: str, expected: object) -> float:
    if metric == "exact": return float(normalized(actual) == normalized(expected))
    if metric == "contains":
        choices = expected if isinstance(expected, list) else [expected]
        return sum(normalized(item) in normalized(actual) for item in choices) / len(choices)
    if metric == "token_f1": return token_f1(actual, str(expected))
    if metric == "valid_json":
        try:
            parsed = json.loads(actual); return float(all(key in parsed for key in (expected or [])))
        except (json.JSONDecodeError, TypeError): return 0.0
    raise ValueError(f"Unknown metric: {metric}")
