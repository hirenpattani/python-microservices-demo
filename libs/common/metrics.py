"""Tiny in-memory metrics collector for demo/testing.

This is intentionally lightweight — for production use a proper metrics client like
prometheus_client and expose a text-format `/metrics` endpoint.
"""

from dataclasses import dataclass, field
from typing import Dict
import time


@dataclass
class Metrics:
    start_time: float = field(default_factory=time.time)
    counters: Dict[str, int] = field(default_factory=dict)

    def inc(self, name: str, amount: int = 1) -> None:
        self.counters[name] = self.counters.get(name, 0) + amount

    def snapshot(self) -> Dict:
        return {
            "uptime_seconds": time.time() - self.start_time,
            "counters": dict(self.counters),
        }
