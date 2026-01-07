import pytest
from services.user_service.app.crud import UserRepository
from services.user_service.app.grpc_service import UserServicer
from services.user_service.app import user_pb2
from libs.common.models import UserCreate


@pytest.fixture
def user_repo():
    """Create a fresh UserRepository for each test."""
    return UserRepository()


@pytest.fixture
async def grpc_servicer(user_repo):
    """Create a gRPC UserServicer."""
    return UserServicer(user_repo)


@pytest.mark.asyncio
async def test_create_user_grpc(user_repo):
    """Test creating a user via gRPC."""
    servicer = UserServicer(user_repo)

    request = user_pb2.UserCreateRequest(name="Alice", email="alice@example.com")
    response = await servicer.CreateUser(request, None)

    assert response.id.startswith("u_")
    assert response.name == "Alice"
    assert response.email == "alice@example.com"


@pytest.mark.asyncio
async def test_get_user_grpc(user_repo):
    """Test getting a user via gRPC."""
    servicer = UserServicer(user_repo)

    # Create user via REST repo
    user = await user_repo.create(UserCreate(name="Bob", email="bob@example.com"))

    # Get user via gRPC
    request = user_pb2.GetUserRequest(user_id=user.id)
    response = await servicer.GetUser(request, None)

    assert response.id == user.id
    assert response.name == "Bob"
    assert response.email == "bob@example.com"


@pytest.mark.asyncio
async def test_list_users_grpc(user_repo):
    """Test listing users via gRPC."""
    servicer = UserServicer(user_repo)

    # Create users
    await user_repo.create(UserCreate(name="Charlie", email="charlie@example.com"))
    await user_repo.create(UserCreate(name="Diana", email="diana@example.com"))

    # List users via gRPC
    request = user_pb2.ListUsersRequest()
    response = await servicer.ListUsers(request, None)

    assert len(response.users) == 2
    assert response.users[0].name in ["Charlie", "Diana"]
    assert response.users[1].name in ["Charlie", "Diana"]


@pytest.mark.asyncio
async def test_user_exists_grpc(user_repo):
    """Test checking user existence via gRPC."""
    servicer = UserServicer(user_repo)

    # Create a user
    user = await user_repo.create(UserCreate(name="Eve", email="eve@example.com"))

    # Check if user exists
    request = user_pb2.UserExistsRequest(user_id=user.id)
    response = await servicer.UserExists(request, None)
    assert response.exists is True

    # Check non-existent user
    request = user_pb2.UserExistsRequest(user_id="u_nonexistent")
    response = await servicer.UserExists(request, None)
    assert response.exists is False
