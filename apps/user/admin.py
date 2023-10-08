from django.contrib import admin
from .models import User


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "username",
        "email",
        "password",
        "created_at",
        "updated_at",
        "subscribed",
    )
    search_fields = (
        "first_name",
        "last_name",
        "username",
        "email",
        "password",
        "created_at",
        "updated_at",
        "subscribed",
    )
    ordering = ("first_name",)
    list_filter = ()
