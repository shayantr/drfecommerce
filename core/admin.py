from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.translation import gettext_lazy as _

from core.models import User, ProductImage, Product


# Register your models here.
class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['phone', 'email', 'password', 'name', 'last_name', 'is_staff', 'is_active']
    fieldsets = (
        (None, {'fields': ('phone', 'email', 'password')}),
        (
            _('Permissions'),
            {'fields': ('is_staff', 'is_active','auth_providers' ,'is_superuser', 'groups', 'user_permissions')}),

    (
        _('Important dates'), {'fields': ('last_login', 'date_joined')}
    )
    )
    readonly_fields = ('last_login', 'date_joined')
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'password1', 'password2', 'is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')
        }),
    )
    form = UserChangeForm
    creation_form = UserCreationForm


admin.site.register(User, UserAdmin)
admin.site.register(ProductImage)
admin.site.register(Product)
