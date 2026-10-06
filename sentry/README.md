# sentry

A Python simulation of Sentry-style error grouping, plus a Java snippet and `.env.example` for wiring the real SDK.

## Goal

Show why errors are grouped by exception type and stack frames rather than by message, so ids inside messages do not split one problem into many issues.

## Run it

```
python3 grouping.py
```

Expected:

```
OK: 4 events grouped into 3 issues; messages with ids share one issue
```

The script ran and passed. It is a model of grouping, not Sentry itself; nothing was sent to a Sentry server and no SDK was compiled.

## What it proves

- `fingerprint()` hashes the exception type plus the stack frames, so the two `PaymentDeclined` events from `Pay.charge:42` and `Order.pay:17` share one issue despite different card numbers and order ids.
- A `PaymentDeclined` thrown from `Pay.retry:61` becomes a separate issue, and the `NullPointerException` another, giving 3 groups of sizes 1, 1 and 2.
- `sentry-init.md` shows `Sentry.init` with `io.sentry:sentry:7.14.0`, reading the DSN from `SENTRY_DSN`; `.env.example` lists that variable with no value.

## Trade-offs

- Real Sentry fingerprints use more inputs (module, function, in-app frames) and can be overridden; this is a simplification.
- Grouping by stack means a refactor that moves a line number starts a new issue.
- The Java snippet is documentation and was not compiled here.

## When not to use it

- If you only need log search, Elasticsearch or Loki already cover it.
- For self-hosting: Sentry's own stack is about 20 containers and is not included; use a free sentry.io project instead.
