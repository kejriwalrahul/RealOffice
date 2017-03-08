from django.conf.urls import url
from rest_framework.authtoken import views as authviews
import views

urlpatterns = [
    url(r'^login/$', authviews.obtain_auth_token),
    url(r'^logout/$', views.LogOutView.as_view(), name='signout'),
    url(r'^dash/$', views.dashboard, name='dashboard'),
]