import json
from pathlib import Path


def test_metrics_valid():
    m = json.loads(Path("artifacts/metrics.json").read_text())
    for k in ["student_id", "accuracy", "training_rows", "model_version", "git_sha"]:
        assert k in m
    assert m["accuracy"] > 0.5
    assert m["training_rows"] >= 100

