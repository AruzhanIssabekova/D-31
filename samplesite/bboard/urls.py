from django.urls import path
from . import views

urlpatterns = [
    path('books_by_author/<int:author_id>/', views.books_by_author, name='books_by_author'),
    path('readers_for_book/<int:book_id>/', views.readers_for_book, name='readers_for_book'),
    path('recent_readers_for_book/<int:book_id>/', views.recent_readers_for_book, name='recent_readers_for_book'),
]
