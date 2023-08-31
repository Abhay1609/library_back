# from django.db import models
#
# class Account(models.Model):
#     name=models.CharField(max_length=100)
#
#     phone=models.IntegerField(max_length=15)
#     email=models.EmailField(max_length=100)
#
#     address=models.CharField(max_length=200)
#
#     college=models.CharField(max_length=150)
#     books=models.ManyToManyField('book.Books',blank=True)
#
# # Create your models here.
from django.db import models
from django.conf import settings

from .managers import MemberManager, LibrarianManager


class Librarian(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    staff_code = models.CharField(max_length=8)

    objects = LibrarianManager()

    def __str__(self):
        return f"Librarian: {self.user.username}"


class Member(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    membership_code = models.CharField(max_length=8)

    objects = MemberManager()

    def __str__(self):
        return f"Member: {self.user.username}"
