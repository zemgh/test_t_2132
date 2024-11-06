from rest_framework import status, mixins, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from books.models import Book
from books.repositories import BookRepository
from books.serializers import BookSerializer, CreateUpdateBookSerializer, BuyBookSerializer

from authors.models import Author
from authors.serializers import AuthorBooksSerializer
from rest_framework.viewsets import GenericViewSet


class BookViewSet(mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet
                  ):

    http_method_names = ['get', 'post', 'put']

    queryset = Book.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['author_id']

    actions_serializers = {
        'list': BookSerializer,
        'create': CreateUpdateBookSerializer,
        'update': CreateUpdateBookSerializer,
        'buy': BuyBookSerializer
    }


    def get_serializer_class(self):
        return self.actions_serializers[self.action]

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


class AuthorViewSet(mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.ListModelMixin,
                    GenericViewSet
                    ):

    http_method_names = ['get', 'post', 'put']
    queryset = Author.objects.all()
    serializer_class = AuthorBooksSerializer