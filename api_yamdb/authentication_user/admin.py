from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User

ADDITIONAL_USER_FIELDS = (
    (None, {'fields': ('bio', 'confirmation_code', 'role')}),
)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User

    list_display = (
        'username', 'email', 'confirmation_code', 'role', 'bio'
    )
    list_editable = (
        'password', 'confirmation_code', 'role', 'is_staff', 'is_active'
    )

