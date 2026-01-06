import contextvars
from typing import Optional

# Context variable for tracking request IDs across async boundaries
_tracking_id: contextvars.ContextVar[Optional[str]] = contextvars.ContextVar(
    "tracking_id", default=None
)


def set_tracking_id(tracking_id: str) -> None:
    """Set the tracking ID for the current request context.

    Args:
        tracking_id: Unique identifier for this request (e.g., "req_abc123").
    """
    _tracking_id.set(tracking_id)


def get_tracking_id() -> Optional[str]:
    """Get the tracking ID for the current request context.

    Returns:
        The tracking ID if set, otherwise None.
    """
    return _tracking_id.get()
