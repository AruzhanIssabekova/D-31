from django.contrib import admin
from .models import Book, Reader, Reading, Author, SpecialReadingEvent, Event

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Reader)
admin.site.register(Reading)
admin.site.register(Event)
admin.site.register(SpecialReadingEvent)