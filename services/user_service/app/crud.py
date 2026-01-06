from typing import Dict, List, Optional

from libs.common.models import User, UserCreate
from libs.common.utils import generate_id


class UserRepository:
    def __init__(self) -> None:
        self._store: Dict[str, User] = {}

    async def create(self, payload: UserCreate) -> User:
        user_id = generate_id("u_")
        # Use `model_dump()` for Pydantic v2 compatibility (replaces `dict()`)
        user = User(id=user_id, **payload.model_dump())
        self._store[user_id] = user
        try:
            # application-level logging (app logger not available here), use module logger
            from libs.common.logging import get_logger

            get_logger(__name__).info("created user %s", user_id)
        except Exception:
            pass
        return user

    async def get(self, user_id: str) -> Optional[User]:
        return self._store.get(user_id)

    async def list_all(self) -> List[User]:
        return list(self._store.values())
