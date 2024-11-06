from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=200, unique=True)
    author = models.ForeignKey('authors.Author', on_delete=models.CASCADE, related_name='books')
    count = models.IntegerField(default=0)

    def __str__(self):
        return self.title