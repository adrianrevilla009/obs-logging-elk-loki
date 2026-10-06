#!/usr/bin/env python3
"""Deterministic head sampling by trace id plus retention policy checks. Run: python3 sampler.py"""
import hashlib, json, pathlib

RATE = {"DEBUG": 0.1, "INFO": 0.25, "WARN": 1.0, "ERROR": 1.0}


def keep(level: str, trace_id: str) -> bool:
    """Hash the trace id so all lines of one trace are kept or dropped together."""
    bucket = int(hashlib.sha256(trace_id.encode()).hexdigest(), 16) % 10_000 / 10_000
    return bucket < RATE[level]


def main() -> None:
    here = pathlib.Path(__file__).parent
    n, kept = 4000, 0
    for i in range(n):
        tid = f"trace-{i}"
        decisions = {keep("INFO", tid) for _ in range(3)}
        assert len(decisions) == 1, "same trace must get same decision"
        kept += decisions.pop()
    ratio = kept / n
    assert 0.20 < ratio < 0.30, ratio
    assert all(keep("ERROR", f"t{i}") for i in range(500)), "errors are never dropped"
    ilm = json.loads((here / "ilm-policy.json").read_text())["policy"]["phases"]
    assert ilm["delete"]["min_age"] == "14d" and "warm" in ilm
    loki = (here / "loki-retention.yml").read_text()
    assert "retention_period: 336h" in loki and "retention_enabled: true" in loki
    print(f"OK: INFO kept {ratio:.1%} (target 25%), ERROR 100%, 14d retention in ILM (14d) and Loki (336h)")


if __name__ == "__main__":
    main()
