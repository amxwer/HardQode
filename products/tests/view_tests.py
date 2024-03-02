from unittest import TestCase

from django.contrib.auth.models import User

from products.models import Product


class ProductTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        testuser1 = User.objects.create_user(
            username='testuser1', password='abc123')
        testuser1.save()
        test_post = Product.objects.create(
            author=testuser1, title='Blog title', body='Body content...')
        test_post.save()