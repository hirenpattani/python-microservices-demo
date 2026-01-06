from typing import Optional

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    """Request model for creating a user.

    Attributes:
        name: User's display name.
        email: User's email address (validated).
    """

    name: str
    email: EmailStr


class User(UserCreate):
    """Response model for a user.

    Attributes:
        id: Unique user identifier.
        name: User's display name.
        email: User's email address.
    """

    id: str


class ProductCreate(BaseModel):
    """Request model for creating a product.

    Attributes:
        name: Product name.
        price: Product price (in currency units).
        user_id: Optional ID of the user who owns this product (foreign key).
    """

    name: str
    price: float
    user_id: Optional[str] = None


class Product(ProductCreate):
    """Response model for a product.

    Attributes:
        id: Unique product identifier.
        name: Product name.
        price: Product price.
        user_id: Optional ID of the user who owns this product.
    """

    id: str
