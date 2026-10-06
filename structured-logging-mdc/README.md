# structured-logging-mdc

A single `Main.java` that prints one JSON object per log line, enriched with request context from a hand-written MDC.

## Goal

Emit JSON log lines that carry `traceId` and `orderId` for every line of a request, so a log shipper can index fields instead of parsing text. The MDC is a plain `ThreadLocal` map, so the folder needs only the JDK and no Logback.

## Run it

```
java Main.java
```

Expected (timestamps and trace ids differ per run):

```
{"ts":"2026-10-05T12:42:28.590781372Z","level":"INFO","traceId":"8d7f1675aa1a4ab7","orderId":"o-1","msg":"order received"}
...
{"ts":"...","level":"INFO","msg":"outside request"}
OK: every request line carries traceId/orderId, MDC cleared afterwards
```

Run with JDK 21; this was run end to end.

## What it proves

- Both lines of order `o-1` share one random 16-hex `traceId`, and `o-2` (handled on a second thread) gets a different one.
- `handleOrder` clears the MDC in a `finally` block, so the "outside request" line has no `traceId` or `orderId`.
- `main` throws `AssertionError` if the last line still contains `traceId`, so the leak check is enforced, not just visible.

## Trade-offs

- The JSON escaping in `esc` only handles backslash, quote and newline; it is fine for a demo, not for arbitrary input.
- A `ThreadLocal` context does not follow work handed to another thread or an async callback; it has to be copied explicitly.
- The trace id is a random UUID slice, not a W3C trace context propagated from a caller.

## When not to use it

- When you already use Logback or Log4j2 with a JSON encoder such as `logstash-logback-encoder`; use `org.slf4j.MDC` there.
- When you need trace ids that cross services; use OpenTelemetry propagation.
