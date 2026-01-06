from dataclasses import dataclass, field
from typing import Dict
from enum import Enum
from collections import defaultdict
import time


class MetricName(Enum):
    """Enum of metric names for type safety."""

    REQUESTS_TOTAL = "requests_total"
    """Total number of HTTP requests processed."""

    def __str__(self) -> str:
        """Return the string value of the enum member.

        Returns:
            The string value (e.g., "requests_total").
        """
        return self.value


@dataclass
class Metrics:
    """In-memory metrics collector for demonstration.

    This class tracks simple metrics like request counts and uptime.
    Each service instance has its own Metrics instance.

    Attributes:
        start_time: Timestamp when the metrics were created (float).
        counters: Dictionary of counter values (str -> int).
    """

    start_time: float = field(default_factory=time.time)
    counters: Dict[str, int] = field(default_factory=lambda: defaultdict(int))

    def inc(self, name: str, amount: int = 1) -> None:
        """Increment a counter by the given amount.

        Args:
            name: Counter name (e.g., "requests_total").
            amount: Amount to increment (default: 1).

        Example:
            >>> m = Metrics()
            >>> m.inc("requests_total")
            >>> m.inc("request_ms_42", 1)
        """
        self.counters[name] += amount

    def snapshot(self) -> Dict:
        """Return a snapshot of current metrics state.

        Returns:
            A dictionary with:
                - uptime_seconds (float): Time elapsed since creation.
                - counters (dict): Copy of all counter values.

        Example:
            >>> m = Metrics()
            >>> m.inc("requests_total", 5)
            >>> snap = m.snapshot()
            >>> snap["uptime_seconds"]  # ~0.001
            >>> snap["counters"]["requests_total"]
            5
        """
        return {
            "uptime_seconds": time.time() - self.start_time,
            "counters": dict(self.counters),
        }
