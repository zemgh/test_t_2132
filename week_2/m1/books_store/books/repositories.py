from django.db import transaction

from .models import Book


class BookRepository:
    def buy_book(self, book: Book, value: int = 1, min_count: int = 0) -> bool:
        with transaction.atomic():
            book = Book.objects.select_for_update().get(id=book.id)

            if book.count - value >= min_count:
                book.count -= value
                book.save()
                return True

            return False
