# loki-promtail

Docker Compose stack (Loki and Promtail 3.2.1) that ships `orders.log` into Loki, with three LogQL queries and an offline check.

## Goal

Show how Promtail parses JSON log lines, promotes `level` to a label and pushes them to Loki, and how LogQL then selects them.

## Run it

```
python3 verify.py
docker compose up -d
python3 verify.py --live
```

Expected from the first command: `OK: loki-promtail config consistent (offline)`. With the stack running, `--live` runs the first query in `queries.logql` against `localhost:3100` and expects exactly one `ERROR` line.

Not run end to end: the containers were not started, so only the offline check was run. The live query is untested.

## What it proves

- `promtail.yml` extracts `level` and `traceId` with a `json` stage and turns only `level` into a label, which keeps label cardinality low.
- `queries.logql` has an error selector, a `| json | traceId="..."` filter to follow one trace, and a `count_over_time` error rate over 5 minutes.
- `verify.py` checks every query is brace-balanced and selects `job="orders"`, and that `orders.log` has exactly one `ERROR` line.

## Trade-offs

- `traceId` stays in the log body and is filtered at query time, which is slower than a label but avoids a stream per trace.
- Offline checks are string matches on the config; they do not validate it against Promtail's schema.
- Loki runs with its default config and no retention; see `log-sampling-retention` for that.

## When not to use it

- If you need full-text search or aggregations over many fields; Elasticsearch fits that better.
- For new setups, check Promtail's status first, as Grafana Alloy is its successor.
