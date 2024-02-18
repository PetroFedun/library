# Library Management System

This Django project is a simple Library Management System that allows users to register as librarians or ordinary guests, view information about books, filter books, manage users, handle orders, and manage authors.

## Features

### User Authentication

- Register as a librarian or a guest user.
- Log in as a guest.
- Log out as an authorized user.

### Books

- View information about all books.
- View details of a specific book.
- Filter books by various criteria (author, title, etc.).
- View all books provided to a specific user (by user ID).

### Users

- View information about all users.
- View details of a specific user.

### Orders

- View information about all orders (for librarians).
- View information about all my orders (for users).
- Create an order (for users).
- Close an order (for librarians).

### Authors

- View information about all authors.
- Create a new author.
- Remove an author if not attached to any book.

## Installation


1. Clone the repository to your local machine:
```
$ git clone https://github.com/PetroFedun/library.git
$ cd library
```
2. Create a virtual environment and activate it:
```
$ python -m venv venv
$ source venv/bin/activate  # On Windows, use 'venv\Scripts\activate'
```
3. Install the project dependencies from the requirements.txt file:
```
$ pip install -r requirements.txt
```
4. Apply the database migrations:
```
$ python manage.py migrate
```
5. Run server:
```
$ python manage.py runserver
```
6. Access the application in your web browser at http://127.0.0.1:8000/user/register/

