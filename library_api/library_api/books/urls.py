from django.urls import path
from .views import (
    LibraryListCreateUpdate, LibraryDetail,
    BookShelfListCreateUpdate, BookShelfDetail,
    AuthorListCreateUpdate, AuthorDetail,
    BookListCreateUpdate, BookDetail
)

urlpatterns = [
    # Library endpoints
    path('libraries/', LibraryListCreateUpdate.as_view(), name='library-list-create-update'),
    path('libraries/<int:pk>/', LibraryDetail.as_view(), name='library-detail'),

    # BookShelf endpoints
    path('bookshelves/', BookShelfListCreateUpdate.as_view(), name='bookshelf-list-create-update'),
    path('bookshelves/<int:pk>/', BookShelfDetail.as_view(), name='bookshelf-detail'),

    # Author endpoints
    path('authors/', AuthorListCreateUpdate.as_view(), name='author-list-create-update'),
    path('authors/<int:pk>/', AuthorDetail.as_view(), name='author-detail'),

    # Book endpoints
    path('books/', BookListCreateUpdate.as_view(), name='book-list-create-update'),
    path('books/<int:pk>/', BookDetail.as_view(), name='book-detail'),
]

