from django.contrib.auth.models import User
from django.db import models

class Product(models.Model):

    Author = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    price = models.DecimalField(max_digits=10,decimal_places=2)
    max_users_per_group = models.PositiveIntegerField(default=5)

    def __str__(self):
        return self.name

class Lesson(models.Model):
    product = models.ForeignKey('Product',on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    link = models.URLField()

    def __str__(self):
        return self.name
# Create your models here.

class Group(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    users = models.ManyToManyField(User)
    max_users = models.PositiveIntegerField(default=5)

    def __str__(self):
        return self.name

    def add_user(self, user):
        self.users.add(user)