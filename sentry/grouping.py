#!/usr/bin/env python3
"""Sentry-style error grouping: fingerprint = exception type + normalised top frames. Run: python3 grouping.py"""
import hashlib, re
from collections import defaultdict

EVENTS = [
    ("PaymentDeclined", "card 4111 declined for order o-1", ["Pay.charge:42", "Order.pay:17"]),
    ("PaymentDeclined", "card 5500 declined for order o-9", ["Pay.charge:42", "Order.pay:17"]),
    ("NullPointerException", "customer is null", ["Order.total:88"]),
    ("PaymentDeclined", "card 4111 declined", ["Pay.retry:61", "Order.pay:17"]),
]


def normalise(msg: str) -> str:
    return re.sub(r"\d+|o-\w+", "<n>", msg)


def fingerprint(exc: str, message: str, frames: list[str]) -> str:
    """Group by type and stack, not by message, so ids in messages do not split issues."""
    return hashlib.sha1("|".join([exc, *frames]).encode()).hexdigest()[:8]


def main() -> None:
    groups = defaultdict(list)
    for exc, msg, frames in EVENTS:
        groups[fingerprint(exc, msg, frames)].append(normalise(msg))
    assert len(groups) == 3, groups
    assert sorted(len(v) for v in groups.values()) == [1, 1, 2]
    print(f"OK: {len(EVENTS)} events grouped into {len(groups)} issues; messages with ids share one issue")


if __name__ == "__main__":
    main()
