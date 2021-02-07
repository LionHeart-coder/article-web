from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        'email', 'first_name', 'last_name',
        'is_active', 'is_staff', 'is_superuser',
    ]
    fieldsets = (
        (_("Personal info"), {
            'fields': (
                'email',
                'first_name',
                'last_name',
                'avatar',
                'password'
            )}),

        (_("Important dates"), {
            'fields': (
                'date_joined',
                'last_login',
            )}
         ),

        (_('Permissions'), {
            'fields': (
                'groups',
                'user_permissions',
                'is_active',
                'is_staff',
                'is_superuser',

            )}
         ),
    )
    list_filter = (
        'is_active',
        'is_staff',
        'is_superuser',
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

    filter_horizontal = ('groups', 'user_permissions')
    readonly_fields = ('date_joined', 'last_login',)
