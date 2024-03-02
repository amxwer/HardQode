from django.contrib.auth.models import User
from rest_framework import serializers
from products.models import Product, Lesson, Group


class ProductSerializer(serializers.ModelSerializer):
    num_lessons = serializers.IntegerField(source='lesson_count')

    class Meta:
        model = Product
        fields = ('Author', 'name', 'start_date', 'price', 'num_lessons')


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model =Lesson

        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class GroupSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True, read_only=True)
    product = ProductSerializer()

    class Meta:
        model = Group
        fields = ['id', 'name', 'users', 'product']


class CustomRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(required=True, write_only=True)
    password2 = serializers.CharField(required=True, write_only=True)
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), required=True)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password1']
        )
        product = validated_data['product']
        product_groups = Group.objects.filter(product=product).order_by('id')
        for group in product_groups:
            if group.users.count() < group.max_users:
                group.users.add(user)
                return user
        new_group = Group.objects.create(product=product, name=f"{product.name} Group")
        new_group.users.add(user)
        return user

