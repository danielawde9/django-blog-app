from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username', 'age', 'is_staff', ] # customize what to show
    fieldsets = UserAdmin.fieldsets + (
            (None, {'fields': ('age',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
            (None, {'fields': ('age',)}),
    )


admin.site.register(CustomUser, CustomUserAdmin)


