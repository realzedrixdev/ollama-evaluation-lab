import sqlite3
from pathlib import Path

from .schema import Result


class Store:
    def __init__(self, path: str | Path):
        self.db = sqlite3.connect(path, check_same_thread=False)
        self.db.execute("PRAGMA journal_mode=WAL")
        self.db.executescript("""
        CREATE TABLE IF NOT EXISTS runs(id TEXT PRIMARY KEY, created_at TEXT, suite TEXT);
        CREATE TABLE IF NOT EXISTS results(
          run_id TEXT, model TEXT, case_id TEXT, response TEXT, score REAL,
          latency_ms REAL, error TEXT, PRIMARY KEY(run_id,model,case_id));
        """)

    def create_run(self, run_id: str, created_at: str, suite: str):
        with self.db: self.db.execute("INSERT INTO runs VALUES(?,?,?)", (run_id, created_at, suite))

    def save(self, result: Result):
        with self.db:
            self.db.execute("INSERT OR REPLACE INTO results VALUES(?,?,?,?,?,?,?)",
                            (result.run_id, result.model, result.case_id, result.response,
                             result.score, result.latency_ms, result.error))

    def rows(self, run_id: str | None = None):
        query = "SELECT run_id,model,case_id,response,score,latency_ms,error FROM results"
        return self.db.execute(query + (" WHERE run_id=?" if run_id else ""), ((run_id,) if run_id else ())).fetchall()

    def runs(self):
        return self.db.execute("SELECT id,created_at,suite FROM runs ORDER BY created_at DESC").fetchall()

    def close(self):
        self.db.close()
