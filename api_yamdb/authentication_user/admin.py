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
    list_editable = ('confirmation_code', 'role')

    add_fieldsets = BaseUserAdmin.add_fieldsets + ADDITIONAL_USER_FIELDS

    fieldsets = BaseUserAdmin.fieldsets + ADDITIONAL_USER_FIELDS
