from rest_framework import serializers

from .models import Book
from authors.models import Author
from authors.serializers import AuthorSerializer


class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(many=False, read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'count']


class CreateUpdateBookSerializer(serializers.ModelSerializer):
    author_id = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all(), source='author', write_only=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'author_id', 'count']


class BuyBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'count']




