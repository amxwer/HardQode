from django.contrib import admin, messages
from .models import Product,Lesson,Group


class GroupAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        print(obj.users.count())
        print(obj.max_users)
        if obj.users.count() > obj.max_users:
            messages.error(request, "Group capacity exceeded. Users cannot be added.")
            return
        else:
            obj.save()

admin.site.register(Product)
admin.site.register(Lesson)
admin.site.register(Group,GroupAdmin)

# Register your models here.
