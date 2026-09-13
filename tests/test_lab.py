import tempfile
import unittest
from pathlib import Path

from model_lab.metrics import score, token_f1
from model_lab.runner import ExperimentRunner
from model_lab.storage import Store


class MockTransport:
    def generate(self, model, prompt, system=""):
        return "42" if "17 + 25" in prompt else '{"language":"ku"}'


class LabTests(unittest.TestCase):
    def test_metrics(self):
        self.assertEqual(score("exact", " 42\n", "42"), 1)
        self.assertGreater(token_f1("هەرێمی کوردستان", "کوردستان"), 0)
        self.assertEqual(score("valid_json", '{"language":"ku"}', ["language"]), 1)

    def test_end_to_end_runner_persists_results(self):
        with tempfile.TemporaryDirectory() as temp:
            suite = Path(temp, "suite.jsonl")
            suite.write_text('{"id":"m1","prompt":"17 + 25","expected":"42","metric":"exact"}\n', encoding="utf-8")
            store = Store(Path(temp, "results.db")); run_id = ExperimentRunner(store, MockTransport()).run(suite, ["mock"])
            rows = store.rows(run_id)
            self.assertEqual(len(rows), 1); self.assertEqual(rows[0][4], 1.0)
            store.close()


if __name__ == "__main__": unittest.main()
