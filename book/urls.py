from django.urls import path, include
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter
from .views import BookViewset, AuthorViewset, BookItemViewSet

from .views import ReservedBookViewset
from .views import FineViewset
from .views import BorrowedBookViewset


router = DefaultRouter()
router.register("borrow_book", BorrowedBookViewset, basename="borrowed-books")
router.register("books", BookViewset, basename="books")
router.register("authors", AuthorViewset, basename="authors")
router.register("fine", FineViewset, basename="fines")
router.register("reserver_books", ReservedBookViewset, basename="reserved-books")
books_router = NestedDefaultRouter(router, "books", lookup="book")
books_router.register("items", BookItemViewSet, basename="book-items")


urlpatterns = [
    path("", include(router.urls)),
    path("", include(books_router.urls)),
]

















