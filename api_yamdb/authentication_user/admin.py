from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


class UserAdmin(BaseUserAdmin):
    model = User
    list_display = (
        'username', 'password', 'email', 'confirmation_code', 'role', 'bio'
    )
    list_editable = ('password', 'confirmation_code', 'role')


admin.site.register(User, UserAdmin)
