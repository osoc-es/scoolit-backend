"""
This is the book module and supports all the REST actions for the
book data
"""

from flask import make_response, abort
from config import db
from models import Book, BookSchema


def read_all():
    """
    This function responds to a request for /api/book
    with the complete lists of books

    :return:        json string of list of people
    """
    # Create the list of books from our data ordered by title
    books = book.query.order_by(book.title).all()

    # Serialize the data for the response
    book_schema = BookSchema(many=True)
    data = book_schema.dump(books)
    return data


def read_one(isbn):
    """
    This function responds to a request for /api/books/{isbn}
    with one matching book from books

    :param isbn:   isbn of books to find
    :return:            book matching id
    """
    # Get the book requested
    book = Book.query.filter(Book.isbn == isbn).one_or_none()

    # Did we find a book?
    if book is not None:

        # Serialize the data for the response
        book_schema = BookSchema()
        data = book_schema.dump(book)
        return data

    # Otherwise, nope, didn't find that person
    else:
        abort(
            404,
            "Book not found for Id: {isbn}".format(isbn=isbn),
        )


def create(book):
    """
    This function creates a new book in the books structure
    based on the passed in book data

    :param book:  book to create in books structure
    :return:        201 on success, 406 on  book exists
    """
    isbn = book.get("isbn")
    title = book.get("title")
    course = book.get("course")
    editorial = book.get("editorial")
    subject = book.get("subject")
    total_quantity = book.get("total_quantity") #TODO Add default 0 and add AutoIncrement every time a sample it's uploaded
    avaliable_quantity = book.get("avaliable_quantity") #TODO Add default 0, add 1 every time a sample it's uploaded and remove 1 every time a sample it's requested.


    existing_book = (
        Book.query.filter(Book.isbn == isbn)
        .one_or_none()
    )

    # Can we insert this book?
    if existing_book is None:

        # Create a book instance using the schema and the passed in book
        schema = BookSchema()
        new_book = schema.load(book, session=db.session)
        # Add the book to the database
        print(new_book)
        db.session.add(new_book)
        db.session.commit()

        # Serialize and return the newly created person in the response
        data = schema.dump(new_book)

        return data, 201

    # Otherwise, nope, book exists already
    else:
        abort(
            409,
            "Book {isbn} exists already".format(
                isbn=isbn
            ),
        )


def update(isbn, book):
    """
    This function updates an existing book in the books structure
    Throws an error if a book with the isbn we want to update to
    already exists in the database.

    :param isbn:   isbn of the book to update in the books structure
    :param book:      book to update
    :return:            updated book structure
    """
    # Get the book requested from the db into session
    update_book = Book.query.filter(
        Book.isbn == isbn
    ).one_or_none()

    # Try to find an existing book with the same isbn as the update
    isbn = book.get("isbn")
    title = book.get("title")

    existing_book = (
        Book.query.filter(Book.isbn == isbn)
        .filter(Book.title == title)
        .one_or_none()
    )

    # Are we trying to find a book that does not exist?
    if update_book is None:
        abort(
            404,
            "Book not found for isbn: {isbn}".format(isbn=isbn),
        )

    # Would our update create a duplicate of another person already existing?
    elif (
        existing_book is not None and str(existing_book.isbn) != str(isbn)
    ):
        abort(
            409,
            "Book with {isbn} and {title} exists already".format(
                isbn=isbn, title=title
            ),
        )

    # Otherwise go ahead and update!
    else:

        # turn the passed in book into a db object
        schema = BookSchema()
        update = schema.load(book, session=db.session)

        # Set the quantities to the book we want to update
        update.total_quantity = update_book.total_quantity + 1
        update.avaliable_quantity = update_book.avaliable_quantity + 1

        # merge the new object into the old and commit it to the db
        db.session.merge(update)
        db.session.commit()

        # return updated book in the response
        data = schema.dump(update_book)

        return data, 200


def delete(isbn):
    """
    This function deletes a book from the books structure

    :param isbn:   isbn of the book to delete
    :return:            200 on successful delete, 404 if not found
    """
    # Get the person requested
    book = Book.query.filter(Book.isbn == isbn).one_or_none()

    # Did we find a person?
    if book is not None:
        db.session.delete(book)
        db.session.commit()
        return make_response(
            "Book {isbn} deleted".format(isbn=isbn), 200
        )

    # Otherwise, nope, didn't find that person
    else:
        abort(
            404,
            "Book not found for isbn: {isbn}".format(isbn=isbn),
        )

