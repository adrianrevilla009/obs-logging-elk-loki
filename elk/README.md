# elk

Docker Compose stack (Elasticsearch, Logstash, Kibana, all 8.15.3) that reads `orders.log`, plus Kibana saved objects and an offline check.

## Goal

Ship JSON order logs through Logstash into daily `orders-*` indices in Elasticsearch, and have a Kibana data view and an errors table ready to import.

## Run it

```
python3 verify.py
docker compose up -d
python3 verify.py --live
```

Expected from the first command: `OK: elk config consistent (offline)`. After the stack is up and Logstash has read the file, `--live` queries `orders-*/_count?q=level:ERROR` and expects exactly 1. In Kibana (`localhost:5601`) use Saved Objects, Import, `dashboard.ndjson`.

Not run end to end: the containers were not started, so only the offline check was run. The live query and the Kibana import are untested.

## What it proves

- `orders.log` has three JSON lines, each with `ts`, `level`, `traceId` and `msg`; one is `ERROR` ("payment declined").
- `logstash.conf` parses with `codec => json`, turns `ts` into `@timestamp` with the `date` filter, and writes to `orders-%{+YYYY.MM.dd}`.
- `dashboard.ndjson` holds an `orders-*` index pattern and a table visualization filtered with `level:ERROR`, and `verify.py` checks both types are present.

## Trade-offs

- Security is off (`xpack.security.enabled: "false"`) and heap is 512 MB, so this is local-only.
- `sincedb_path => "/dev/null"` re-reads the file on every restart, which duplicates documents.
- The visualization is a bare table definition, not a styled dashboard, and the ILM policy from `log-sampling-retention` is not attached here.

## When not to use it

- For a production cluster; it has a single node, no auth and no persistence volume.
- For container logs at scale, where a lighter shipper such as Filebeat or Loki is a better fit than Logstash.
