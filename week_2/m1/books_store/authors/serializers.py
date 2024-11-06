from rest_framework import serializers

from .models import Author


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class AuthorBooksSerializer(AuthorSerializer):
    books = serializers.StringRelatedField(many=True, read_only=True)
