__all__ = (
    'CommentForm',
    'BlogForm',
    'SingUpForm',
    'LoginForm',
    'EditUserForm',
    'ResetEmailForm',
    'ResetPasswordForm',
    'TagForm',
    'CreateSuperUserForm',
)

from .blogs import CommentForm, BlogForm, TagForm
from .accounts import SingUpForm, LoginForm, EditUserForm, ResetEmailForm, ResetPasswordForm, CreateSuperUserForm
