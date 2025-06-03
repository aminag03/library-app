from fastapi import FastAPI, Depends, HTTPException
from typing import List
from fastapi.responses import Response
from sqlalchemy.orm import Session
from sql_app.database import Base, SessionLocal, engine
from sql_app import schemas, crud, models
from sql_app.routers import users
from sql_app.routers.common import get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)

Base.metadata.create_all(bind=engine)


@app.post("/authors/", response_model=schemas.Author)
def create_author_api(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    db_author = crud.create_author(db=db, author=author)
    if db_author is None:
        raise HTTPException(status_code=404, detail="This author already exists in database!")
    return Response(content=f"Author \"{author.first_name} {author.last_name}\" added successfully!", status_code=200)


# If pagination parameters are null, first 10 authors will be returned.
@app.get("/authors", response_model=List[schemas.Author])
def get_authors_api(page: int = 1, pageSize: int = 10, db: Session = Depends(get_db)):
    db_authors = crud.get_authors(db=db)

    start_index = (page - 1) * pageSize
    end_index = start_index + pageSize

    return db_authors[start_index:end_index]


@app.post("/categories/", response_model=schemas.Category)
def create_category_api(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    db_category = crud.create_category(db=db, category=category)
    if db_category is None:
        raise HTTPException(status_code=404, detail="This category already exists in database!")
    return Response(content=f"Category \"{category.name}\" added successfully!", status_code=200)


@app.get("/categories", response_model=List[schemas.Category])
def get_categories_api(page: int = 1, pageSize: int = 10, db: Session = Depends(get_db)):
    db_categories = crud.get_categories(db=db)

    start_index = (page - 1) * pageSize
    end_index = start_index + pageSize

    return db_categories[start_index:end_index]


@app.post("/books/", response_model=schemas.Book)
def create_book_api(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db=db, book=book)


@app.get("/books", response_model=List[schemas.Book])
def get_books_api(page: int = 1, pageSize: int = 10, db: Session = Depends(get_db)):
    db_books = crud.get_books(db=db)

    start_index = (page - 1) * pageSize
    end_index = start_index + pageSize

    return db_books[start_index:end_index]


@app.post("/book_items/")
def create_book_item_api(book_item_data: schemas.BookItemDTO, db: Session = Depends(get_db)):
    db_book_item, book_name = crud.create_book_item(db=db, book_item=schemas.BookItemCreate(**book_item_data.dict()))
    if db_book_item is None:
        raise HTTPException(status_code=404, detail="Book with provided ID does not exist! Please enter an existing "
                                                    + "book_id. If your book is not in database, please create a new "
                                                    + "Book before proceeding!")
    return Response(content=f"Book Item \"{book_name}\" added successfully!", status_code=200)


@app.post("/user_book_item/")
def create_user_book_item_api(user_book_item_data: schemas.UserBookItemDTO, db: Session = Depends(get_db)):
    return crud.create_user_book_item(user_book_item_data=user_book_item_data, db=db)


@app.get("/user_book_items", response_model=List[schemas.BookItem])
def get_active_user_book_items_by_user_id_api(user_id: int, page: int = 1, pageSize: int = 10, db: Session = Depends(get_db)):
    db_user_book_items = crud.get_active_user_book_items_by_user_id(user_id=user_id, db=db)
    if db_user_book_items is None:
        return HTTPException(status_code=404, detail="User not found! Please enter existing user_id.")

    start_index = (page - 1) * pageSize
    end_index = start_index + pageSize

    return db_user_book_items[start_index:end_index]


@app.put("/users/{user_id}/books/{book_item_id}")
def return_book_item_api(user_id: int, book_item_id: int, db: Session = Depends(get_db)):
    return crud.return_book_item(db=db, user_id=user_id, book_item_id=book_item_id)
