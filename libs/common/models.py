from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    name: str
    email: EmailStr


class User(UserCreate):
    id: str


class ProductCreate(BaseModel):
    name: str
    price: float


class Product(ProductCreate):
    id: str
