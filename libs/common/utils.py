import uuid


def generate_id(prefix: str = ""):  # -> str
    """Generate a short unique identifier with an optional prefix."""
    uid = uuid.uuid4().hex[:8]
    return f"{prefix}{uid}" if prefix else uid
