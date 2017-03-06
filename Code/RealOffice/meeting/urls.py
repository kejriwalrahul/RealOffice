from django.conf.urls import url
from rest_framework.authtoken import views

urlpatterns = [
    url(r'^login/$', views.obtain_auth_token),
]