import sqlite3
from pathlib import Path
from .models import RunResult

def save(result: RunResult, db_path: str | Path = "procurepilot.db") -> None:
    with sqlite3.connect(db_path) as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS runs (run_id TEXT PRIMARY KEY, created_at TEXT NOT NULL, data TEXT NOT NULL)")
        conn.execute("INSERT OR REPLACE INTO runs VALUES (?, ?, ?)", (result.run_id, result.created_at.isoformat(), result.model_dump_json()))

def list_runs(db_path: str | Path = "procurepilot.db") -> list[tuple[str,str]]:
    with sqlite3.connect(db_path) as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS runs (run_id TEXT PRIMARY KEY, created_at TEXT NOT NULL, data TEXT NOT NULL)")
        return conn.execute("SELECT run_id, created_at FROM runs ORDER BY created_at DESC").fetchall()

def load(run_id: str, db_path: str | Path = "procurepilot.db") -> RunResult:
    with sqlite3.connect(db_path) as conn:
        row = conn.execute("SELECT data FROM runs WHERE run_id=?", (run_id,)).fetchone()
    if row is None: raise KeyError(run_id)
    return RunResult.model_validate_json(row[0])
