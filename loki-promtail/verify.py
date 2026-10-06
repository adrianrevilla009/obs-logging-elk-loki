#!/usr/bin/env python3
"""Offline: check promtail config, log file and LogQL selectors agree.
--live runs the first LogQL query against Loki on localhost:3100 after `docker compose up -d`."""
import json, pathlib, re, sys, time, urllib.parse, urllib.request

d = pathlib.Path(__file__).parent
cfg = (d / "promtail.yml").read_text()
assert "http://loki:3100/loki/api/v1/push" in cfg and "job: orders" in cfg
assert "- labels:" in cfg, "level must be promoted to a label"
rows = [json.loads(l) for l in (d / "orders.log").read_text().splitlines()]
queries = [q for q in (d / "queries.logql").read_text().splitlines() if q]
for q in queries:
    assert q.count("{") == q.count("}") and re.search(r'job="orders"', q), q
errors = [r for r in rows if r["level"] == "ERROR"]
assert len(errors) == 1
if "--live" in sys.argv:
    url = "http://localhost:3100/loki/api/v1/query_range?" + urllib.parse.urlencode(
        {"query": queries[0], "start": str(time.time_ns() - 3600 * 10**9)})
    res = json.load(urllib.request.urlopen(url))["data"]["result"]
    assert sum(len(s["values"]) for s in res) == 1, res
print("OK: loki-promtail config consistent" + (" and live query matched" if "--live" in sys.argv else " (offline)"))
