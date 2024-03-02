from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.datetime_safe import date

from .models import Group, Product
from .views import GroupManager
from django.utils import timezone

@receiver(post_save, sender=Group)
def handle_new_user_in_group(sender, instance, created, **kwargs):
    if created:
        if instance.users.count() >= instance.product.max_users_per_group:
            new_group = Group.objects.create(product=instance.product, name=f"{instance.product.name} Group")
            new_group.users.add(instance.users.last())


@receiver(post_save, sender=Group)
def check_group_capacity(sender, instance, created, **kwargs):
    if created:
        if instance.users.count() > 5:
            raise Exception("Group capacity exceeded")


@receiver(post_save, sender=Product)
def redistribute_users(sender, instance, created, **kwargs):
    if not created:
        if instance.start_date.date() == date.today():
            groups = Group.objects.filter(product=instance)
            group_manager = GroupManager()
            group_manager.redistribute_users_to_groups(groups)
