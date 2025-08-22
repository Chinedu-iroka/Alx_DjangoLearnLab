from django.contrib import admin

# Register your models here.

from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'followers_count')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('bio', 'profile_picture', 'followers')}),
    )
    filter_horizontal = ('followers',)

admin.site.register(CustomUser, CustomUserAdmin)