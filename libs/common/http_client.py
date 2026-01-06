import httpx


async def check_user_exists(
    user_id: str, user_service_url: str = "http://localhost:8001"
) -> bool:
    """Check if a user exists by calling the User service.

    Args:
        user_id: The user ID to verify.
        user_service_url: Base URL of the User service (default: localhost:8001).

    Returns:
        True if the user exists, False otherwise.

    Raises:
        httpx.RequestError: If the request to User service fails.

    Example:
        >>> exists = await check_user_exists("u_abc123")
        >>> if exists:
        ...     print("User found!")
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{user_service_url}/users/{user_id}")
            return response.status_code == 200
        except httpx.RequestError:
            # In production, handle timeouts, retries, circuit breakers, etc.
            return False
