from sqlalchemy import Column, ForeignKey, Boolean, Integer, String, Date, DateTime
from sqlalchemy.orm import relationship
from sql_app.database import Base


class UserBookItem(Base):
    __tablename__ = "user_book_items"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    book_item_id = Column(Integer, ForeignKey("book_items.id"), primary_key=True)
    borrow_date = Column(Date, primary_key=True)
    borrow_status = Column(Boolean)


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String, index=True, nullable=False)
    last_name = Column(String, index=True, nullable=False)
    birth_date = Column(Date, nullable=False)
    biography = Column(String)

    books = relationship("Book", back_populates="author")


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String, index=True)
    language = Column(String, index=True)
    publication_date = Column(Date, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    author_id = Column(Integer, ForeignKey("authors.id"), nullable=False)

    category = relationship("Category", back_populates="books")
    author = relationship("Author", back_populates="books")
    book_items = relationship("BookItem", back_populates="book")


class BookItem(Base):
    __tablename__ = "book_items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    available = Column(Boolean, default=True, nullable=False)
    publisher = Column(String, nullable=False)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)

    book = relationship("Book", back_populates="book_items")
    users = relationship("User", secondary="user_book_items", back_populates="book_items")



class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, index=True, nullable=False)

    books = relationship("Book", back_populates="category")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String, index=True, nullable=False)
    last_name = Column(String, index=True, nullable=False)
    email = Column(String, nullable=False)
    status = Column(Boolean, nullable=False)
    membership_renewal_date = Column(Date, nullable=False)
    penalties = Column(Integer)

    book_items = relationship("BookItem", secondary="user_book_items", back_populates="users")
