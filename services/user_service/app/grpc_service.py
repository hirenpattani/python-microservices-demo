import grpc

from libs.common.logging import get_logger
from services.user_service.app.crud import UserRepository
from services.user_service.app import user_pb2, user_pb2_grpc

logger = get_logger(__name__)


class UserServicer(user_pb2_grpc.UserServiceServicer):
    """gRPC service implementation for User operations."""

    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def CreateUser(
        self, request: user_pb2.UserCreateRequest, context: grpc.aio.ServicerContext
    ) -> user_pb2.User:
        """Create a new user.

        Args:
            request: UserCreateRequest with name and email.
            context: gRPC context.

        Returns:
            User: Created user with ID.
        """
        from libs.common.models import UserCreate

        payload = UserCreate(name=request.name, email=request.email)
        user = await self.repo.create(payload)
        logger.info(f"Created user via gRPC: {user.id}")
        return user_pb2.User(id=user.id, name=user.name, email=user.email)

    async def GetUser(
        self, request: user_pb2.GetUserRequest, context: grpc.aio.ServicerContext
    ) -> user_pb2.User:
        """Get a user by ID.

        Args:
            request: GetUserRequest with user_id.
            context: gRPC context.

        Returns:
            User: User details.

        Raises:
            RpcError: If user not found.
        """
        user = await self.repo.get(request.user_id)
        if not user:
            await context.abort(grpc.StatusCode.NOT_FOUND, "User not found")
        logger.info(f"Retrieved user via gRPC: {user.id}")
        return user_pb2.User(id=user.id, name=user.name, email=user.email)

    async def ListUsers(
        self, request: user_pb2.ListUsersRequest, context: grpc.aio.ServicerContext
    ) -> user_pb2.ListUsersResponse:
        """List all users.

        Args:
            request: ListUsersRequest.
            context: gRPC context.

        Returns:
            ListUsersResponse: List of all users.
        """
        users = await self.repo.list_all()
        user_messages = [
            user_pb2.User(id=u.id, name=u.name, email=u.email) for u in users
        ]
        logger.info(f"Listed {len(users)} users via gRPC")
        return user_pb2.ListUsersResponse(users=user_messages)

    async def UserExists(
        self, request: user_pb2.UserExistsRequest, context: grpc.aio.ServicerContext
    ) -> user_pb2.UserExistsResponse:
        """Check if a user exists.

        Args:
            request: UserExistsRequest with user_id.
            context: gRPC context.

        Returns:
            UserExistsResponse: Boolean indicating if user exists.
        """
        user = await self.repo.get(request.user_id)
        exists = user is not None
        logger.info(f"Checked user existence via gRPC: {request.user_id} -> {exists}")
        return user_pb2.UserExistsResponse(exists=exists)
