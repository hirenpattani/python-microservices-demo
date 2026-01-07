import httpx
import grpc


async def check_user_exists(
    user_id: str, user_service_url: str = "http://localhost:8001"
) -> bool:
    """Check if a user exists by calling the User service via REST.

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


async def check_user_exists_grpc(
    user_id: str, user_service_url: str = "localhost:50051"
) -> bool:
    """Check if a user exists by calling the User service via gRPC.

    Args:
        user_id: The user ID to verify.
        user_service_url: gRPC endpoint of the User service (default: localhost:50051).

    Returns:
        True if the user exists, False otherwise.

    Raises:
        grpc.RpcError: If the gRPC call fails.

    Example:
        >>> exists = await check_user_exists_grpc("u_abc123")
        >>> if exists:
        ...     print("User found!")
    """
    # Import here to avoid circular imports and grpc availability checks
    from services.user_service.app import user_pb2, user_pb2_grpc

    try:
        async with (
            grpc.aio.secure_channel(
                user_service_url, grpc.aio.ssl_channel_credentials()
            )
            if ":" in user_service_url and user_service_url.endswith(":443")
            else grpc.aio.insecure_channel(user_service_url)
        ) as channel:
            stub = user_pb2_grpc.UserServiceStub(channel)
            request = user_pb2.UserExistsRequest(user_id=user_id)
            response = await stub.UserExists(request)
            return response.exists
    except grpc.RpcError:
        # In production, handle retries, circuit breakers, etc.
        return False
