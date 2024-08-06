from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User
    list_display = (
        'username', 'password',
        'email', 'confirmation_code',
        'role', 'bio',
        'is_staff', 'is_active'
    )
    list_editable = (
        'password', 'confirmation_code', 'role', 'is_staff', 'is_active'
    )

