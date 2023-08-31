# from rest_framework import serializers
# from .models import Account
# class accountSerializers(serializers.ModelSerializer):
#     class Meta:
#         model=Account
#         fields="__all__"
from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer

from .models import Librarian, Member


class UserSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id", "username", "password", "email", "first_name", "last_name")


class CreateMemberSerializer(ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Member
        fields = ("user",)

    def save(self, **kwargs):
        user = self.validated_data["user"]
        self.instance = Member.objects.create_member(
            username=user["username"],
            password=user["password"],
            email=user["email"],
            first_name=user["first_name"],
            last_name=user["last_name"],
        )
        return self.instance


class MemberSerializer(ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Member
        fields = ("id", "membership_code", "user")


class CreateLibrarianSerializer(ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Member
        fields = ("user",)

    def create(self, validated_data):
        user = validated_data["user"]
        return Librarian.objects.create_librarian(
            username=user["username"],
            password=user["password"],
            email=user["email"],
            first_name=user["first_name"],
            last_name=user["last_name"],
        )


class LibrarianSerializer(ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Librarian
        fields = ("id", "staff_code", "user")
from rest_framework import serializers

from account.serializers import MemberSerializer
from book.serializers import BorrowedBookSerializer

from book.models import BookItem
from book.models import Fine


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
