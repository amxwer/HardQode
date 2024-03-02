from django.utils import timezone

from rest_framework.response import Response
from rest_framework import generics, permissions, status
from django.db.models import Count
from products.models import Product, Lesson, Group
from products.permissions import LessonPermission
from products.serializers import ProductSerializer, LessonSerializer, GroupSerializer, CustomRegisterSerializer


class ProductAPIView(generics.ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.annotate(lesson_count=Count('lesson'))


class LessonListAPIView(generics.ListAPIView):
    permission_classes = [LessonPermission]
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

    def filter_queryset(self, queryset):
        product_name = self.kwargs['product_name']  # Получаем имя продукта из URL
        return Lesson.objects.filter(product__name__iexact=product_name)


class GroupListAPIView(generics.ListAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CustomRegisterAPIView(generics.CreateAPIView):
    serializer_class = CustomRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({"message": "User successfully registered."}, status=status.HTTP_201_CREATED)


class GroupManager:
    @classmethod
    def redistribute_users_to_groups(cls, groups):
        all_users = GroupManager.get_unique_users(groups)
        total_users_count = len(all_users)
        groups_count = len(groups)
        users_per_group = total_users_count // groups_count
        remaining_users = total_users_count % groups_count


        for group in groups:
            group_users_count = users_per_group
            if remaining_users > 0:
                group_users_count += 1
                remaining_users -= 1


            cls.assign_users_to_group(group, all_users[:group_users_count])

            all_users = all_users[group_users_count:]

    @staticmethod
    def get_unique_users(groups):

        unique_users = set()
        all_users = [user for group in groups for user in group.users.all()]

        if not all_users:
            return []


        users_per_group = len(all_users) // len(groups)
        remaining_users = len(all_users) % len(groups)

        for i, group in enumerate(groups):
            start_index = i * users_per_group + min(i, remaining_users)
            end_index = start_index + users_per_group + (1 if i < remaining_users else 0)
            unique_users.update(all_users[start_index:end_index])

        return list(unique_users)

    @staticmethod
    def assign_users_to_group(group, users):
        group.users.clear()
        for user in users:

            if group.product in user.groups.all():
                group.users.add(user)


