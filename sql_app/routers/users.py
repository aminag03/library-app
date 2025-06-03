from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import Response
from sql_app import crud, schemas
from sql_app.routers.common import get_db
from sqlalchemy.orm import Session

router = APIRouter()

router = APIRouter(
    prefix="/users",
    tags=["User Endpoints"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=schemas.UserDTO)
def create_user_api(user_data: schemas.UserDTO, db: Session = Depends(get_db)):
    db_user = crud.create_user(db=db, user=schemas.UserCreate(**user_data.dict()))
    if db_user is None:
        raise HTTPException(status_code=404, detail="User with this email address already exists."
                                                    + " Please use a different email address.")
    return \
        Response(content=f"User \"{user_data.first_name} {user_data.last_name}\" added successfully!", status_code=200)


# If pagination parameters are null, first 10 users will be returned.
@router.get("/", response_model=list[schemas.User])
def get_users_api(page: int = 1, pageSize: int = 10, db: Session = Depends(get_db)):
    db_users = crud.get_users(db=db)

    start_index = (page - 1) * pageSize
    end_index = start_index + pageSize

    return db_users[start_index:end_index]


@router.get("/by_status", response_model=list[schemas.User])
def get_users_by_status_api(status: bool, page: int = 1, pageSize: int = 10, db: Session = Depends(get_db)):
    db_users = crud.get_users_by_status(status=status, db=db)

    start_index = (page - 1) * pageSize
    end_index = start_index + pageSize

    return db_users[start_index:end_index]