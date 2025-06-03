from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from sql_app import models
from sql_app import schemas
import os
from dotenv import load_dotenv
from datetime import date, timedelta

load_dotenv()

MAX_NUMBER_OF_BOOKS = int(os.getenv("MAX_NUMBER_OF_BOOKS"))
MAX_NUMBER_OF_DAYS = int(os.getenv("MAX_NUMBER_OF_DAYS"))
MEMBERSHIP_DURATION_DAYS = int(os.getenv("MEMBERSHIP_DURATION_DAYS"))


def create_user(db: Session, user: schemas.UserCreate):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user is None:
        db_user = models.User(**user.dict())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    return None


def get_users(db: Session):
    return db.query(models.User).all()


def get_users_by_status(db: Session, status: bool):
    return db.query(models.User).filter(models.User.status == status).all()


def create_author(db: Session, author: schemas.AuthorCreate):
    existing_author = db.query(models.Author).filter(models.Author.first_name == author.first_name). \
        filter(models.Author.last_name == author.last_name).filter(models.Author.birth_date == author.birth_date). \
        first()

    if existing_author is None:
        db_author = models.Author(**author.dict())
        db.add(db_author)
        db.commit()
        db.refresh(db_author)
        return db_author
    return None


def get_authors(db: Session):
    return db.query(models.Author).all()


def create_category(db: Session, category: schemas.CategoryCreate):
    existing_category = db.query(models.Category).filter(models.Category.name == category.name).first()

    if existing_category is None:
        db_category = models.Category(**category.dict())
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        return db_category
    return None


def get_categories(db: Session):
    return db.query(models.Category).all()


def create_book(db: Session, book: schemas.BookCreate):
    author = db.query(models.Author).filter(models.Author.id == book.author_id).first()
    if author is None:
        return HTMLResponse(content="Author with provided ID does not exist! Please enter an existing author_id.")

    category = db.query(models.Category).filter(models.Category.id == book.category_id).first()
    if category is None:
        categories = db.query(models.Category).all()
        category_list = "\n".join([f"{category.id}: {category.name}" for category in categories])

        message = (
            "Category with provided ID does not exist! Please enter an existing category_id.\n"
            f"Here are existing categories and their IDs: \n{category_list}\n"
            "If your category is not on this list, create a new category and then proceed."
        )
        return HTMLResponse(content=message)

    db_book = models.Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_books(db: Session):
    return db.query(models.Book).all()


def create_book_item(db: Session, book_item: schemas.BookItemCreate):
    book = db.query(models.Book).filter(models.Book.id == book_item.book_id).first()
    if book is None:
        return None, None
    db_book_item = models.BookItem(**book_item.dict())
    db.add(db_book_item)
    db.commit()
    db.refresh(db_book_item)
    return db_book_item, book.title


def create_user_book_item(db: Session, user_book_item_data: schemas.UserBookItemDTO):
    user = db.query(models.User).filter(models.User.id == user_book_item_data.user_id).first()
    book = db.query(models.Book).filter(models.Book.title == user_book_item_data.book_title).first()

    if user is None:
        return HTMLResponse(content="User not found! Please enter existing user_id!")
    if book is None:
        return HTMLResponse(content="Book not found! Please make sure that you have entered book_title correctly.")

    if (user.membership_renewal_date + timedelta(days=MAX_NUMBER_OF_DAYS)) < date.today():
        return HTMLResponse(content="Your membership has expired! Please renew your membership before proceeding.")

    current_user_book_items = db.query(models.UserBookItem).filter(models.UserBookItem.user_id == user.id). \
        filter(models.UserBookItem.borrow_status == True).count()

    if current_user_book_items == MAX_NUMBER_OF_BOOKS:
        return HTMLResponse(content=f"You already have {MAX_NUMBER_OF_BOOKS} borrowed books! " +
                                    "You must return at least 1 before proceeding.")

    for user_book_item in db.query(models.UserBookItem).filter(models.UserBookItem.user_id == user.id). \
            filter(models.UserBookItem.borrow_status == True).all():
        if (user_book_item.borrow_date + timedelta(days=MAX_NUMBER_OF_DAYS)) < date.today():
            return HTMLResponse(content="You must return all due books before borrowing new one!")

    book_item = db.query(models.BookItem).filter(models.BookItem.book_id == book.id). \
        filter(models.BookItem.available == True).first()
    if book_item is None:
        return HTMLResponse(content="The book you're looking for is not available at the moment.")

    book_item.available = False
    db_user_book_item = \
        models.UserBookItem(user_id=user.id, book_item_id=book_item.id, borrow_date=date.today(), borrow_status=True)
    db.add(db_user_book_item)
    db.commit()
    db.refresh(db_user_book_item)
    return HTMLResponse(content=f"Book borrowed successfully! Keep in mind that you have to return it by " +
                                f"{db_user_book_item.borrow_date + timedelta(MAX_NUMBER_OF_DAYS)} at the latest.")


def get_active_user_book_items_by_user_id(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        return None

    book_items = user.book_items

    return book_items


def return_book_item(db: Session, user_id: int, book_item_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    book_item = db.query(models.BookItem).filter(models.BookItem.id == book_item_id).first()

    if user is None:
        return HTMLResponse(content="User not found! Please enter existing user_id!")
    if book_item is None:
        return HTMLResponse(content="BookItem not found! Please enter existing book_item_id!")

    user_book_item = db.query(models.UserBookItem).filter(models.UserBookItem.user_id == user_id,
                                                          models.UserBookItem.book_item_id == book_item_id,
                                                          models.UserBookItem.borrow_status == True).first()

    book = db.query(models.Book).filter(models.Book.id == book_item.book_id).first()

    if user_book_item is None:
        return \
            HTMLResponse(content=f"Selected book_item is not currently borrowed by {user.first_name} {user.last_name}")

    # user_book_item.borrow_status = False
    book_item.available = True
    db.delete(user_book_item)
    db.commit()
    db.refresh(book_item)
    return HTMLResponse(content=f"{book.title} returned successfully!")
