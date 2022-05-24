from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.html import format_html

from .models import User
from .forms import CustomUserCreationForm, CustomUserChangeForm

CustomUser = get_user_model()


@admin.register(User)
class UserAdmin(UserAdmin):

    def thumbnail(self, obj: User):
        return format_html(f'<img src="{obj.photo.url}" width="100" />')

    def full_name(self, obj):
        return str(obj)

    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'first_name',
                'last_name',
                'birthday',
                'photo',
                'phone',
                'user_type',
                'is_active',
                'is_admin',
                'is_staff',
                'is_superuser',
            ),
        }),
    )

    thumbnail.short_description = 'Фото'
    full_name.short_description = 'ФИО'

    list_display = ('thumbnail', 'email', 'full_name', 'birthday')
    list_display_links = ('thumbnail', 'email')
    search_fields = ('first_name', 'last_name')

    ordering = ('email',)
    exclude = ('groups', 'user_permissions')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.unregister(Group)
