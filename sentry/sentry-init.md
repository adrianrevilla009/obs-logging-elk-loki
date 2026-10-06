Wiring the real SDK (Java 21, pinned `io.sentry:sentry:7.14.0`); the DSN comes from the environment, never from git:

```java
Sentry.init(o -> {
    o.setDsn(System.getenv("SENTRY_DSN"));   // see .env.example
    o.setRelease("orders@1.0.0");
    o.setTracesSampleRate(0.1);
});
```

Self-hosted Sentry is a ~20-container stack (`getsentry/self-hosted`); it is not included here. Use a free sentry.io project instead.
