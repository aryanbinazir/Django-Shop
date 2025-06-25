from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserCreationForms, UserChangeForm
from .models import User, OtpCode
from django.contrib.auth.models import Group

class UserAdmin(BaseUserAdmin):
    create_form = UserCreationForms
    change_form = UserChangeForm

    list_display = ('email', 'phone_number', 'is_admin')
    list_filter = ('is_admin',)

    fieldsets = (
        (None, {'fields': ('phone_number', 'email', 'full_name', 'password',)}),
        ("Permissions", {'fields': ('is_active', 'is_admin', 'is_superuser', 'last_login', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {'fields': ('phone_number', 'email', 'full_name', 'password1', 'password2')}),

    )

    search_fields = ['full_name', 'email']
    ordering = ['full_name']
    filter_horizontal = ('groups', 'user_permissions')
    readonly_fields = ('last_login',)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            form.base_fields['is_superuser'].disabled = True
        return form

admin.site.register(User, UserAdmin)

@admin.register(OtpCode)
class OtpCodeAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'code', 'created')