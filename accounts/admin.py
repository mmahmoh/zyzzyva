from django.contrib import admin
from django_use_email_as_username.admin import BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'phone', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    search_fields = ('email', 'first_name', 'last_name', 'phone')
    ordering = ('email',)

    def get_fieldsets(self, request, obj=None):
        if [_ for _ in request.get_full_path().split('/') if _].pop() == 'change':
            fieldsets = list(super().get_fieldsets(request, obj))
            fieldsets.pop(1)
            fieldsets.insert(1, ('Personal info', {'fields': ('first_name', 'last_name', 'phone')}))
            return tuple(fieldsets)
        return super().get_fieldsets(request, obj)
