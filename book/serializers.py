# from .models import Books , Categories
# from rest_framework import serializers
# class BookSerializers(serializers.ModelSerializer):
#     class Meta:
#         model=Books
#         fields="__all__"
# class CategorySerializers(serializers.ModelSerializer):
#     class Meta:
#         model=Categories
#         fields="__all__"
from rest_framework import serializers

from .models import BookItem
from .models import BorrowedBook


class BookItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookItem
        fields = ("id", "book", "barcode", "status", "publication_date")


class BorrowedBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowedBook
        fields = ("id", "book_item", "borrower", "borrowed_date", "due_date")

    book_item = BookItemSerializer()


class BorrowedBookCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowedBook
        fields = ("book_item", "borrower", "borrowed_date", "due_date")
from rest_framework import serializers

from .models import Book, BookItem, Author


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ("id", "name", "description")


class AuthorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ("id", "name", "description", "books")


class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(many=True)

    class Meta:
        model = Book
        fields = ("id", "title", "isbn", "author", "subject", "page_counts")


class BookCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ("title", "isbn", "author", "subject", "page_counts")


class BookItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookItem
        fields = ("id", "book", "barcode", "status", "publication_date")

    book = BookSerializer()


class BookItemCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookItem
        fields = ("id", "barcode", "status", "publication_date")

    def create(self, validated_data):
        book_id = self.context["book_id"]
        return BookItem.objects.create(book_id=book_id, **validated_data)
from rest_framework import serializers

from .models import BookItem
from .models import ReservedBook


class BookItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookItem
        fields = ("id", "book", "barcode", "status", "publication_date")


class ReservedBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservedBook
        fields = ("id", "book_item", "reserver", "reserved_at", "due_time")

    book_item = BookItemSerializer()


class ReservedBookCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservedBook
        fields = ("book_item", "reserver", "reserved_at", "due_time")
from rest_framework import serializers

from account.serializers import MemberSerializer
from .serializers import BorrowedBookSerializer

from .models import BookItem
from .models import Fine


class BookItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookItem
        fields = ("id", "book", "barcode", "status", "publication_date")


class FineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fine
        fields = ("id", "member", "borrowed_book", "amount")

    member = MemberSerializer()
    borrowed_book = BorrowedBookSerializer()
