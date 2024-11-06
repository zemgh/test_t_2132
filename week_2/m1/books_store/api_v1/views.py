from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from books.models import Book
from books.repositories import BookRepository
from books.serializers import BookSerializer, CreateUpdateBookSerializer, BuyBookSerializer

from authors.models import Author
from authors.serializers import AuthorBooksSerializer


class BookViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'put']
    queryset = Book.objects.all()

    def get_serializer_class(self):
        if self.action in ('create', 'update'):
            return CreateUpdateBookSerializer
        elif self.action == 'buy':
            return BuyBookSerializer
        return BookSerializer

    @action(['POST'], detail=True)
    def buy(self, request, pk=None):
        book = self.get_object()

        repo = BookRepository()
        result = repo.buy_book(book)

        if result:
            return Response(
                status=status.HTTP_200_OK
            )

        return Response(
            data={'error': 'out of stock'},
            status=status.HTTP_400_BAD_REQUEST
        )


class AuthorViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'put']
    queryset = Author.objects.all()
    serializer_class = AuthorBooksSerializer