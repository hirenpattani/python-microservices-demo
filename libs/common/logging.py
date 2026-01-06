import logging
from typing import Optional

from libs.common.context import get_tracking_id


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """Return a configured logger instance with tracking ID support.

    Args:
        name: Logger name (defaults to "python-microservices-demo").

    Returns:
        A configured logging.Logger instance.

    Note:
        Uses INFO level by default. In production, configure via environment
        variables or a logging config file. Logs include tracking_id from
        contextvars if set.
    """
    logger = logging.getLogger(name or "python-microservices-demo")
    if not logger.handlers:
        handler = logging.StreamHandler()
        # Include tracking_id if available in the context
        fmt = "[%(tracking_id)s] %(asctime)s %(levelname)s %(name)s: %(message)s"
        formatter = logging.Formatter(fmt, defaults={"tracking_id": "no-track"})
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        # Add a filter to inject tracking_id from context
        class TrackingIdFilter(logging.Filter):
            def filter(self, record):
                tracking_id = get_tracking_id()
                record.tracking_id = tracking_id or "no-track"
                return True

        logger.addFilter(TrackingIdFilter())

    logger.setLevel(logging.INFO)
    return logger
