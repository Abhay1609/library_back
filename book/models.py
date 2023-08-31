from django.db import models
from datetime import date

from django.core.validators import MinValueValidator
class Author(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Author: {self.name}"
class Book(models.Model):
    title = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True)
    author = models.ManyToManyField(Author, related_name="books")
    subject = models.CharField(max_length=127)
    page_counts = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Book: {self.title}"
class BookItem(models.Model):
    STATUS_AVAILABLE = "A"
    STATUS_BORROWED = "B"
    STATUS_RESERVED = "R"
    STATUS_LOST = "L"

    STATUS_CHOICES = (
        (STATUS_AVAILABLE, "Available"),
        (STATUS_BORROWED, "Borrowed"),
        (STATUS_RESERVED, "Reserved"),
        (STATUS_LOST, "Lost"),
    )
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="book_items")
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    publication_date = models.DateField()
    barcode = models.CharField(max_length=15, unique=True)
    def is_available(self):
        return self.status == self.STATUS_AVAILABLE

    def change_status(self, to: str):
        self.status = to
        self.save(update_fields=["status"])

    def __str__(self):
        return f"BookItem: {self.book.title}"

class BorrowedBook(models.Model):
    book_item = models.OneToOneField(BookItem, on_delete=models.CASCADE)
    borrower = models.ForeignKey("account.Member", on_delete=models.CASCADE)
    borrowed_date = models.DateField(auto_now_add=True)
    due_date = models.DateField(validators=[MinValueValidator(date.today)])

    def is_due_date_past(self):
        if self.due_date < date.today():
            return True
        return False

    def how_many_days_past_from_due_date(self):
        td = date.today() - self.due_date
        if td.days >= 0:
            return td.days

    def __str__(self):
        return (
            f"{self.book_item.book.title} borrowed from {self.borrower.user.username}"
        )
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator


class ReservedBook(models.Model):
    book_item = models.OneToOneField(BookItem, on_delete=models.CASCADE)
    reserver = models.ForeignKey("account.Member", on_delete=models.SET_NULL, null=True)
    reserved_at = models.DateTimeField(auto_now_add=True)
    due_time = models.DateTimeField(validators=[MinValueValidator(timezone.now)])

    def __str__(self):
        return (
            f"{self.id}"
        )

from decimal import Decimal
from django.db import models


class Fine(models.Model):
    member = models.ForeignKey("account.Member", on_delete=models.CASCADE)
    borrowed_book = models.OneToOneField(
        BorrowedBook, on_delete=models.CASCADE, unique=True
    )
    amount = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)

    @staticmethod
    def calculate_fine(borrowed_book) -> Decimal:
        past_days_count = borrowed_book.how_many_days_past_from_due_date()
        return Decimal(past_days_count * 5.00)

    def __str__(self) -> str:
        return f"Fine: {self.amount} for {self.member}"
