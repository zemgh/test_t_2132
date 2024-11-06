import pytest
from rest_framework import status

from books.models import Book

from authors.models import Author

BASE_URL = '/api/v1/'


@pytest.mark.django_db
def test_books_list(api_client, books):
    url = BASE_URL + 'books/'

    books_count = Book.objects.count()

    # Список Book
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == books_count


@pytest.mark.django_db
def test_filter_books_by_author(api_client, books, author):
    url = BASE_URL + 'books/'

    books_count = Book.objects.filter(author__id=author.id).count()
    author_2 = Author.objects.create(first_name='test fname', last_name='test lname')

    # Получение списка Book по Author.id
    response = api_client.get(url + f'?author_id={author.id}')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == books_count

    response = api_client.get(url + f'?author_id={author_2.id}')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 0

    # Получение списка Book по невалидному Author.id
    response = api_client.get(url + f'?author_id={author_2.id + 1}')
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_create_book(api_client, author):
    url = BASE_URL + 'books/'

    objects_count = Book.objects.count()
    data = {
        'title': 'test_new_create_book',
        'author_id': author.id,
        'count': 100500
    }

    # создание Book
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert Book.objects.count() == objects_count + 1

    # создание Book с неуникальным title
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_update_book(api_client, book):
    url = BASE_URL + f'books/{book.id}/'

    new_title = 'test_create_book'
    data = {
        'title': new_title,
        'author_id': book.author.id,
        'count': book.count + 1
    }

    # Обновление Book
    response = api_client.put(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['title'] == data['title']
    assert response.data['count'] == data['count']


@pytest.mark.django_db
def test_buy_book(api_client, book):
    url = BASE_URL + f'books/{book.id}/buy/'

    count = book.count
    data = {
        'count': 1
    }

    # Покупка Book
    response = api_client.post(url, data=data, format='json')
    assert response.status_code == status.HTTP_200_OK
    book = Book.objects.get(id=book.id)
    assert book.count == count - 1

    # Покупка Book при нулевом count
    response = api_client.post(url, data=data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['error'] == 'out of stock'


@pytest.mark.django_db
def test_authors_list(api_client, author):
    url = BASE_URL + 'authors/'

    authors_count = Author.objects.count()

    # Cписок Author
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == authors_count
    books = response.data[0]['books']
    for book in books:
        assert type(book) == str


@pytest.mark.django_db
def test_author_create(api_client):
    url = BASE_URL + 'authors/'

    authors_count = Author.objects.count()
    data = {
        'first_name': 'test fname',
        'last_name': 'test lname'
    }

    # Создание Author
    response = api_client.post(url, data=data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert Author.objects.count() == authors_count + 1



@pytest.mark.django_db
def test_author_update(api_client, author):
    url = BASE_URL + f'authors/{author.id}/'

    new_fname = 'test_new_fname'
    data = {
        'first_name': new_fname,
        'last_name': 'test lname'
    }

    # Обновление Author
    response = api_client.put(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['first_name'] == new_fname
