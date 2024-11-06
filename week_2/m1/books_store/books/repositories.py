from .models import Book


class BookRepository:
    def buy_book(self, book: Book, value: int = 1, min_count: int = 0) -> bool:

        if book.count - value >= min_count:
            book.count -= value
            book.save()
            return True

        return False
