# Library Management API

This is a lightweight backend application built with **FastAPI** for managing a small library system. It provides a RESTful API for handling users, authors, books, book copies (items), categories, and borrow/return logic. The app uses **PostgreSQL** as the database and **SQLAlchemy** as the ORM.

## Description

The application supports:

- Creating and retrieving users, authors, books, and categories
- Borrowing and returning books with status and due date tracking
- Enforcing membership duration and borrowing limits via environment configuration
- Basic validation to ensure book availability and user eligibility

There is no frontend; interaction is done entirely through API endpoints. Swagger documentation is automatically available at `/docs`.

## Technologies Used

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- dotenv (for configuration)

## Environment Configuration

The following environment variables are used to control borrowing policies:

- `MAX_NUMBER_OF_BOOKS`: Maximum number of books a user can borrow
- `MAX_NUMBER_OF_DAYS`: Maximum borrowing period per book
- `MEMBERSHIP_DURATION_DAYS`: Membership validity duration

