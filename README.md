# obs-logging-elk-loki

Five small folders that show how structured logs get produced, shipped to Elasticsearch or Loki, sampled, expired and grouped into errors, all around a tiny Orders example.

## What is inside

| Folder | What it shows | Run |
| --- | --- | --- |
| [`structured-logging-mdc`](./structured-logging-mdc) | JSON log lines enriched with `traceId` and `orderId` from a thread-local MDC | `java Main.java` |
| [`elk`](./elk) | Logstash pipeline into Elasticsearch, Kibana saved objects, compose file | `python3 verify.py` (add `--live` after `docker compose up -d`) |
| [`loki-promtail`](./loki-promtail) | Promtail JSON pipeline into Loki and three LogQL queries | `python3 verify.py` (add `--live` after `docker compose up -d`) |
| [`log-sampling-retention`](./log-sampling-retention) | Trace-consistent sampling plus 14-day retention in an ILM policy and in Loki | `python3 sampler.py` |
| [`sentry`](./sentry) | Error grouping by exception type and stack, and how to wire the Sentry SDK | `python3 grouping.py` |

## Prerequisites

- Java 21 (only for `structured-logging-mdc`; it runs as a single source file)
- Python 3.10 or newer (standard library only)
- Docker with Compose, only for the live checks in `elk` and `loki-promtail`

## How to read it

Start with `structured-logging-mdc` to see the log format, then read `elk` and `loki-promtail` side by side: both ship the same `orders.log` shape through different stacks. The compose stacks were not started when these READMEs were written; each folder says exactly what was run.
