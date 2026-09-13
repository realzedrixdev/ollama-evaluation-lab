from dataclasses import dataclass, field


@dataclass(frozen=True)
class Case:
    id: str
    prompt: str
    expected: object
    metric: str = "exact"
    weight: float = 1.0
    system: str = ""
    tags: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class Result:
    run_id: str
    model: str
    case_id: str
    response: str
    score: float
    latency_ms: float
    error: str | None = None
