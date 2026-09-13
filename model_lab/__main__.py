import argparse
import json
from pathlib import Path

from .report import build_report
from .runner import ExperimentRunner
from .storage import Store


def main():
    parser = argparse.ArgumentParser(description="Benchmark local Ollama models")
    commands = parser.add_subparsers(dest="command", required=True)
    run = commands.add_parser("run"); run.add_argument("suite"); run.add_argument("--models", required=True)
    run.add_argument("--db", default="results.db"); run.add_argument("--workers", type=int, default=2)
    report = commands.add_parser("report"); report.add_argument("--db", default="results.db"); report.add_argument("--run")
    report.add_argument("--output", default="report.html")
    history = commands.add_parser("history"); history.add_argument("--db", default="results.db")
    args = parser.parse_args(); store = Store(args.db)
    if args.command == "run":
        print(json.dumps({"run_id": ExperimentRunner(store, workers=args.workers).run(args.suite, args.models.split(","))}))
    elif args.command == "report":
        Path(args.output).write_text(build_report(store.rows(args.run)), encoding="utf-8"); print(args.output)
    else:
        for row in store.runs(): print("\t".join(row))


if __name__ == "__main__": main()
