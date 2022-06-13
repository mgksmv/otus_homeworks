from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from config.settings import DEBUG
from onlineschool.views import HomeTemplateView, Contact

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('', HomeTemplateView.as_view(), name='home'),
    path('accounts/', include('accounts.urls')),
    path('courses/', include('onlineschool.urls')),
    path('contact/', Contact.as_view(), name='contact')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if DEBUG:
    urlpatterns += [path('__debug__/', include('debug_toolbar.urls'))]
