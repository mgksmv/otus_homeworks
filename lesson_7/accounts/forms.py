from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

CustomUser = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = (
            'email',
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
        )
