from django.conf import settings
from django.urls import include, path, register_converter
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.urlpatterns import format_suffix_patterns

from . import converter
from . import views

register_converter(converter.StatusConverter, 'conv')

# API endpoints
urlpatterns = [
    path('api/user/login/', obtain_auth_token, name='login-user'),
    path('api/user/', views.UserRegisterView.as_view(), name='register-user'),
    path('favicon/.ico', RedirectView.as_view(
        url='/static/icons/favicon.ico',
        permanent=True
        )),
    path('', TemplateView.as_view(template_name='index.html')),
    path('api/dog/<pk>/<conv:status>/', views.UpdateStatus.as_view(),
         name='update_status'),

    path('api/dog/<pk>/<conv:status>/next/', views.Dogs.as_view(),
         name='next_undecided'),

    path('api/user/preferences/', views.CreateUpdatePreference.as_view(),
         name='preferences')
    ]
if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
                      path('__debug__/', include(debug_toolbar.urls))
                      ] + urlpatterns
urlpatterns = format_suffix_patterns(urlpatterns)
