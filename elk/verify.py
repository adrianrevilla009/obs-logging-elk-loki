#!/usr/bin/env python3
"""Offline check: log lines are valid JSON with trace ids, compose/pipeline/dashboard are consistent.
Add --live to also query Elasticsearch on localhost:9200 after `docker compose up -d`."""
import json, pathlib, sys, urllib.request

d = pathlib.Path(__file__).parent
rows = [json.loads(l) for l in (d / "orders.log").read_text().splitlines()]
assert all({"ts", "level", "traceId", "msg"} <= r.keys() for r in rows), "log line missing field"
conf = (d / "logstash.conf").read_text()
assert "codec => json" in conf
assert "orders-%{+YYYY.MM.dd}" in conf
objs = [json.loads(l) for l in (d / "dashboard.ndjson").read_text().splitlines()]
assert {o["type"] for o in objs} == {"index-pattern", "visualization"}
assert "elasticsearch:8.15.3" in (d / "docker-compose.yml").read_text()
if "--live" in sys.argv:
    q = urllib.request.urlopen("http://localhost:9200/orders-*/_count?q=level:ERROR").read()
    assert json.loads(q)["count"] == 1, q
print("OK: elk config consistent" + (" and live query matched" if "--live" in sys.argv else " (offline)"))
