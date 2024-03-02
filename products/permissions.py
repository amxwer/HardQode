from rest_framework import permissions
from products.models import Group


class LessonPermission(permissions.BasePermission):



        def has_permission(self, request, view):
            product_name = view.kwargs.get('product_name')
            print(product_name)
            user = request.user
            print(user)
            if not product_name or not user.is_authenticated:
                return False

            product_groups = Group.objects.filter(product__name__iexact=product_name, users=user)
            print(product_groups)
            return product_groups.exists()