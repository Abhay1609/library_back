# from django.shortcuts import render
# from .models import Account
# from .serializers import accountSerializers
# from rest_framework import viewsets
# class accountviewset(viewsets.ModelViewSet):
#     queryset=Account.objects.all()
#     serializer_class = accountSerializers
#
# # Create your views here.
from django.contrib.auth import get_user_model

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser

from .models import Librarian, Member
from .permissions import IsAdminOrLibrarian
from .serializers import (
    MemberSerializer,
    CreateMemberSerializer,
    LibrarianSerializer,
    CreateLibrarianSerializer,
)


User = get_user_model()


class MemberViewset(ModelViewSet):
    queryset = Member.objects.select_related("user").all()
    permission_classes = [IsAdminOrLibrarian]

    def get_serializer_class(self):
        if self.action == "create":
            return CreateMemberSerializer
        return MemberSerializer

    def perform_destroy(self, instance):
        instance.user.delete()
        return super().perform_destroy(instance)


class LibrarianViewset(ModelViewSet):
    queryset = Librarian.objects.select_related("user").all()
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        if self.action == "create":
            return CreateLibrarianSerializer
        return LibrarianSerializer

    def perform_destroy(self, instance):
        instance.user.delete()
        return super().perform_destroy(instance)
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins

from account.permissions import IsAdminOrLibrarian
from book.models import Fine
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
