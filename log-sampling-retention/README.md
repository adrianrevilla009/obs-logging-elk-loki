# log-sampling-retention

A small sampler script plus an Elasticsearch ILM policy and a Loki retention config that all agree on 14 days.

## Goal

Cut log volume by sampling per trace rather than per line, and expire old logs with the same 14-day window in both stacks.

## Run it

```
python3 sampler.py
```

Expected:

```
OK: INFO kept 24.9% (target 25%), ERROR 100%, 14d retention in ILM (14d) and Loki (336h)
```

The script ran and passed. The ILM policy and the Loki config were only read as files; neither was loaded into a running Elasticsearch or Loki.

## What it proves

- `keep()` hashes the trace id with SHA-256, so every line of one trace gets the same decision; 4000 traces at the 25% INFO rate kept 24.9%.
- `ERROR` and `WARN` have a rate of 1.0, so the script asserts 500 error traces are all kept.
- `ilm-policy.json` rolls over daily, force-merges at 3 days and deletes at 14 days; `loki-retention.yml` sets `336h` (14 days) and keeps `{level="ERROR"}` streams for `720h`.

## Trade-offs

- Head sampling decides before the outcome is known; a trace that later fails can already have lost its INFO lines.
- The 25% rate is hard-coded in `RATE`, and the 4000 traces are synthetic, not taken from `orders.log`.
- The checks compare strings in the files, so a typo that still contains the expected text would pass.

## When not to use it

- When you must keep every line for audit; sampling would drop data.
- When you need tail sampling based on the final outcome of a trace; that needs a collector such as OpenTelemetry's.
