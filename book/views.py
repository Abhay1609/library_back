# from django.shortcuts import render
# from rest_framework import viewsets
# from .models import Categories,Books
# from .serializers import BookSerializers,CategorySerializers
# class booksviewset(viewsets.ModelViewSet):
#     serializer_class = BookSerializers
#     queryset = Books.objects.all()
# class categoriesviewset(viewsets.ModelViewSet):
#     serializer_class = CategorySerializers
#     queryset = Categories.objects.all()
# # Create your views here.
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins

from account.permissions import IsAdminOrLibrarian
from .models import BorrowedBook
from .serializers import BorrowedBookSerializer, BorrowedBookCreateSerializer


class BorrowedBookViewset(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = BorrowedBook.objects.select_related("book_item").all()
    permission_classes = [IsAdminOrLibrarian]

    def get_serializer_class(self):
        if self.action in ("create"):
            return BorrowedBookCreateSerializer
        return BorrowedBookSerializer
from rest_framework.viewsets import ModelViewSet

from .models import Book, BookItem, Author
from .filters import AuthorFilter, BookFilter, BookItemFilter
from .serializers import (
    BookSerializer,
    BookCreateUpdateSerializer,
    AuthorSerializer,
    AuthorListSerializer,
    BookItemSerializer,
    BookItemCreateUpdateSerializer,
)


class BookViewset(ModelViewSet):
    queryset = Book.objects.prefetch_related("author").all()
    filterset_class = BookFilter

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return BookCreateUpdateSerializer
        return BookSerializer


class AuthorViewset(ModelViewSet):
    filterset_class = AuthorFilter

    def get_queryset(self):
        if self.action == "list":
            Author.objects.prefetch_related("books").all()
        return Author.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return AuthorListSerializer
        return AuthorSerializer


class BookItemViewSet(ModelViewSet):
    filterset_class = BookItemFilter

    def get_queryset(self):
        return (
            BookItem.objects
                .select_related("book")
                .prefetch_related("book__author")
                .filter(book=self.kwargs["book_pk"])
        )

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return BookItemCreateUpdateSerializer
        return BookItemSerializer

    def get_serializer_context(self):
        return {"book_id": self.kwargs["book_pk"]}
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins

from account.permissions import IsAdminOrLibrarian

from .models import ReservedBook
from .serializers import ReservedBookSerializer, ReservedBookCreateSerializer


class ReservedBookViewset(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = ReservedBook.objects.select_related("book_item").all()
    permission_classes = [IsAdminOrLibrarian]

    def get_serializer_class(self):
        if self.action in ("create"):
            return ReservedBookCreateSerializer
        return ReservedBookSerializer
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins

from account.permissions import IsAdminOrLibrarian
from .models import Fine
from .serializers import FineSerializer


class FineViewset(
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = Fine.objects.select_related(
        "member",
        "member__user",
        "borrowed_book",
        "borrowed_book__book_item"
    ).all()
    serializer_class = FineSerializer
    permission_classes = [IsAdminOrLibrarian]
