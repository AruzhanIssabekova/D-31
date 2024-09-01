from datetime import date
from django.shortcuts import render, get_object_or_404
from .models import Author
from .models import Reader, Book, Reading, SpecialReadingEvent
from django.db import transaction, IntegrityError




def create_special_reading_event(reader, book, description, date, extra_notes=None):
    try:
        with transaction.atomic():
            reading, created = Reading.objects.get_or_create(
                reader=reader,
                book=book,
                start_date=date
            )
            if not reading:
                raise ValueError("Не удалось создать или получить объект чтения")
            special_event = SpecialReadingEvent.objects.create(
                description=description,
                date=date,
                reading=reading,
                extra_notes=extra_notes
            )
            if not special_event or special_event.some_field == 'invalid_value':
                raise IntegrityError("Недопустимое значение для специального события")

            return special_event

    except IntegrityError:
        print("Ошибка: транзакция откатится")
        return None


def books_by_author(request, author_id):
    author = get_object_or_404(Author, id=author_id)
    books = Book.objects.filter(authors=author).prefetch_related('authors')
    return render(request, 'books_by_author.html', {'author': author, 'books': books})

def readers_for_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    readers = Reading.objects.filter(book=book).select_related('reader')
    return render(request, 'readers_for_book.html', {'book': book, 'readers': readers})

def recent_readers_for_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    recent_readings = Reading.objects.filter(book=book, start_date__gt=date(2024, 8, 1)).select_related('reader')
    return render(request, 'recent_readers_for_book.html', {'book': book, 'recent_readings': recent_readings})

