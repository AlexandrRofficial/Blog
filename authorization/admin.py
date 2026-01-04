from django.contrib import admin

from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_staff')
    readonly_fields = ('role',)

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser