from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import MyUser, File

@admin.register(MyUser)
class MyUserAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'email', 'is_ops_user')
    list_filter = ('is_ops_user', 'is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_ops_user')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'is_staff', 'is_superuser', 'is_ops_user'),
        }),
    )
    search_fields = ('username', 'email', 'first_name')
    ordering = ('username',)
# file_sharing_project/admin.py
from django.contrib import admin

admin.autodiscover()
admin.site.register(File)