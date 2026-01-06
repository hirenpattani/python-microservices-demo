import uuid


def generate_id(prefix: str = "") -> str:
    """Generate a short unique identifier with an optional prefix.

    Uses UUID4 (random UUID) and takes the first 8 hex characters for brevity
    while maintaining uniqueness.

    Args:
        prefix: Optional prefix for the ID (e.g., "u_" for users, "p_" for products).

    Returns:
        A unique ID string in the format: "{prefix}{8-char-hex}"
        Example: "u_550e8400" or "550e8400" (if prefix is empty).

    Example:
        >>> user_id = generate_id("u_")
        >>> user_id.startswith("u_")
        True
        >>> len(user_id)  # "u_" (2) + 8 hex chars
        10

        >>> product_id = generate_id("p_")
        >>> product_id.startswith("p_")
        True
    """
    uid = uuid.uuid4().hex[:8]
    return f"{prefix}{uid}" if prefix else uid
