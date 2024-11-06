import pytest

from rest_framework.test import APIClient

from authors.models import Author

from books.models import Book


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def author():
    return Author.objects.create(first_name='test_fname', last_name='test_lname')


@pytest.fixture
def books(author):
    return Book.objects.bulk_create(
        [
            Book(title='test_book_1', author=author, count=1),
            Book(title='test_book_2', author=author, count=1)]
    )


@pytest.fixture
def book(books):
    return books[0]

