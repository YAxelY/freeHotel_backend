from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, HotelOwner

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Permissions', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'is_hotel_owner',
                'groups',
                'user_permissions'
            ),
        }),
        ('Dates', {'fields': ('last_login', 'created_at')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'username', 'is_staff', 'is_hotel_owner')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'is_hotel_owner')
    search_fields = ('email', 'username')
    ordering = ('-created_at',)
    readonly_fields = ('last_login', 'created_at')

@admin.register(HotelOwner)
class HotelOwnerAdmin(admin.ModelAdmin):
    list_display = ('user', 'business_name', 'contact_number')
    search_fields = ('user__email', 'business_name')

admin.site.register(User, CustomUserAdmin)