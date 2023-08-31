from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Author, Book, BookItem


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "isbn",
        "subject",
        "page_counts",
    )

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "description",
    )

@admin.register(BookItem)
class MemberAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "book_id",
        "barcode",
        "status",
        "publication_date",
    )
from django.contrib import admin

from .models import ReservedBook


@admin.register(ReservedBook)
class ReservedBookAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "book_item_id",
        "reserver_id",
        "reserved_at",
        "due_time",
    )
from django.contrib import admin

from .models import Fine


@admin.register(Fine)
class MemberAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "borrowed_book",
        "member_id",
        "amount",
    )
