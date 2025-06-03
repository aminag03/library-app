from pydantic import BaseModel, EmailStr, Field
from datetime import date
from typing import List, Optional
import datetime


class UserBookItemBase(BaseModel):
    borrow_status: bool = Field(default=True)


class UserBookItemCreate(UserBookItemBase):
    pass


class UserBookItem(UserBookItemBase):
    user_id: int
    book_item_id: int
    borrow_date: date = Field(default=date.today())

    class Config:
        from_attributes = True


class BookItemBase(BaseModel):
    available: bool = Field(default=True)
    publisher: str
    book_id: int


class BookItemCreate(BookItemBase):
    pass


class BookItem(BookItemBase):
    id: int

    class Config:
        from_attributes = True


class BookBase(BaseModel):
    title: str
    publication_date: date
    description: Optional[str] = None
    language: Optional[str] = None
    category_id: int
    author_id: int


class BookCreate(BookBase):
    pass


class Book(BookBase):
    id: int
    book_items: List[BookItem] = []

    class Config:
        from_attributes = True


class AuthorBase(BaseModel):
    first_name: str
    last_name: str
    birth_date: date
    biography: Optional[str] = None


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int
    books: List[Book] = []

    class Config:
        from_attributes = True


class CategoryBase(BaseModel):
    name: str


class CategoryCreate(CategoryBase):
    pass


class Category(CategoryBase):
    id: int
    books: List[Book] = []

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    status: bool = Field(default=True)
    membership_renewal_date: date = Field(default=date.today())
    penalties: int = Field(default=0)


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int

    class Config:
        from_attributes = True


class UserDTO(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr


class BookItemDTO(BaseModel):
    publisher: str
    book_id: int


class UserBookItemDTO(BaseModel):
    user_id: int
    book_title: str
