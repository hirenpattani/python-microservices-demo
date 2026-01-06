from fastapi import APIRouter, Depends, HTTPException
from libs.common.models import UserCreate, User
from services.user_service.app.crud import UserRepository
from typing import List

router = APIRouter()


# Single repository instance for demo/testing purposes
_repo = UserRepository()


def get_repo():
    """Dependency that returns the shared repository instance."""
    return _repo


@router.post("/", response_model=User)
async def create_user(
    payload: UserCreate, repo: UserRepository = Depends(get_repo)
) -> User:
    user = await repo.create(payload)
    return user


@router.get("/", response_model=List[User])
async def list_users(repo: UserRepository = Depends(get_repo)) -> List[User]:
    return await repo.list_all()


@router.get("/{user_id}", response_model=User)
async def get_user(user_id: str, repo: UserRepository = Depends(get_repo)) -> User:
    user = await repo.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    return user
