from __future__ import annotations

import json
import time
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

from .metrics import score
from .schema import Case, Result
from .storage import Store
from .transport import OllamaTransport


def load_suite(path: str | Path) -> list[Case]:
    return [Case(**json.loads(line)) for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()]


class ExperimentRunner:
    def __init__(self, store: Store, transport=None, workers: int = 2):
        self.store = store
        self.transport = transport or OllamaTransport()
        self.workers = workers

    def _execute(self, run_id: str, model: str, case: Case) -> Result:
        started = time.perf_counter()
        try:
            response = self.transport.generate(model, case.prompt, case.system)
            error = None; value = score(case.metric, response, case.expected)
        except Exception as exc:
            response = ""; error = f"{type(exc).__name__}: {exc}"; value = 0.0
        return Result(run_id, model, case.id, response, value,
                      (time.perf_counter() - started) * 1000, error)

    def run(self, suite_path: str | Path, models: list[str]) -> str:
        cases, run_id = load_suite(suite_path), uuid.uuid4().hex[:12]
        self.store.create_run(run_id, datetime.now(timezone.utc).isoformat(), str(suite_path))
        with ThreadPoolExecutor(max_workers=self.workers) as pool:
            futures = [pool.submit(self._execute, run_id, model, case) for model in models for case in cases]
            for future in as_completed(futures): self.store.save(future.result())
        return run_id
