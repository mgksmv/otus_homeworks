from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.authtoken.views import obtain_auth_token
from graphene_django.views import GraphQLView

from config.settings import DEBUG
from config.api.views import APIRootView
from onlineschool.views import HomeTemplateView, Contact, APITemplateView, generate_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('', HomeTemplateView.as_view(), name='home'),
    path('accounts/', include('accounts.urls')),
    path('courses/', include('onlineschool.urls')),
    path('contact/', Contact.as_view(), name='contact'),
    path('api-token/', APITemplateView.as_view(), name='api_token'),
    path('generate-token/', generate_token, name='generate_token'),

    # Rest Framework
    path('api-auth/', include('rest_framework.urls')),
    path('api-token-auth/', obtain_auth_token),
    path('api/v1/', APIRootView.as_view(), name='api_root_view'),
    path('api/v1/', include('onlineschool.api.urls')),
    path('api/v1/', include('accounts.api.urls')),

    # GraphQL
    path('graphql/', GraphQLView.as_view()),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if DEBUG:
    urlpatterns += [path('__debug__/', include('debug_toolbar.urls'))]
    urlpatterns.insert(0, path('graphql/', GraphQLView.as_view(graphiql=True)))
