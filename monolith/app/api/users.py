from typing import List

from fastapi import APIRouter, Depends, HTTPException

from libs.common.models import UserCreate, User
from monolith.app.crud import UserRepository

router = APIRouter()

_repo = UserRepository()


def get_repo() -> UserRepository:
    """Dependency injection for UserRepository."""
    return _repo


@router.post("", response_model=User)
async def create_user(payload: UserCreate, repo: UserRepository = Depends(get_repo)):
    """Create a new user.

    Args:
        payload: UserCreate with name and email.
        repo: Injected UserRepository.

    Returns:
        User: Created user with ID.
    """
    return await repo.create(payload)


@router.get("/{user_id}", response_model=User)
async def get_user(user_id: str, repo: UserRepository = Depends(get_repo)):
    """Get a user by ID.

    Args:
        user_id: User ID to retrieve.
        repo: Injected UserRepository.

    Returns:
        User: User details.

    Raises:
        HTTPException: 404 if user not found.
    """
    user = await repo.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("", response_model=List[User])
async def list_users(repo: UserRepository = Depends(get_repo)):
    """List all users.

    Args:
        repo: Injected UserRepository.

    Returns:
        List[User]: All users in the system.
    """
    return await repo.list_all()
