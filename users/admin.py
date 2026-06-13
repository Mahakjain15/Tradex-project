from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Post


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display  = ('email', 'username', 'get_full_name', 'is_staff', 'date_joined')
    list_filter   = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering      = ('-date_joined',)
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'bio', 'avatar')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display  = ('user', 'text_snippet', 'created_at', 'updated_at')
    list_filter   = ('created_at',)
    search_fields = ('user__username', 'text')
    readonly_fields = ('created_at', 'updated_at')

    def text_snippet(self, obj):
        return obj.text[:60] + '...' if len(obj.text) > 60 else obj.text
    text_snippet.short_description = 'Content'
