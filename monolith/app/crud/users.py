from typing import Dict, List, Optional

from libs.common.models import User, UserCreate
from libs.common.utils import generate_id
from libs.common.logging import get_logger

logger = get_logger(__name__)


class UserRepository:
    def __init__(self) -> None:
        self._store: Dict[str, User] = {}

    async def create(self, payload: UserCreate) -> User:
        """Create a new user.

        Args:
            payload: UserCreate model with name and email.

        Returns:
            User: Created user with generated ID.
        """
        user_id = generate_id("u_")
        user = User(id=user_id, **payload.model_dump())
        self._store[user_id] = user
        logger.info(f"Created user: {user_id}")
        return user

    async def get(self, user_id: str) -> Optional[User]:
        """Get a user by ID.

        Args:
            user_id: The user ID to retrieve.

        Returns:
            User or None if not found.
        """
        return self._store.get(user_id)

    async def list_all(self) -> List[User]:
        """List all users.

        Returns:
            List of all users in repository.
        """
        return list(self._store.values())
