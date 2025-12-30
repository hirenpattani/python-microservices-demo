"""Small logging helper to provide a consistent logger across services."""

import logging
from typing import Optional


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """Return a configured logger instance.

    - Uses INFO level by default for demo. In production, configure via env vars or a logging config file.
    """
    logger = logging.getLogger(name or "python-microservices-demo")
    if not logger.handlers:
        handler = logging.StreamHandler()
        fmt = "%(asctime)s %(levelname)s %(name)s: %(message)s"
        handler.setFormatter(logging.Formatter(fmt))
        logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger
