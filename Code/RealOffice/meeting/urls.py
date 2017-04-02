from django.conf.urls import url
from rest_framework.authtoken import views as authviews
import views

urlpatterns = [
    url(r'^$', views.loginpage, name='loginpage'),
    url(r'^login/$', authviews.obtain_auth_token),
    url(r'^logout/$', views.LogOutView.as_view(), name='signout'),
    
    url(r'^dash/$', views.dashboard, name='dashboard'),
    
    url(r'^user/usrdash/$', views.UserInfo.as_view(), name='usrinfo'),
    url(r'^user/change_pass/$', views.ChangePassword.as_view(), name='change_password'),
    
    url(r'^person/check/$', views.CheckPerson.as_view(), name='check_people'),
    url(r'^person/add/$', views.AddPerson.as_view(), name='add_person'),

    url(r'^meeting/add/$', views.AddMeeting.as_view(), name='add_meeting'),

    url(r'^report/$', views.Report.as_view(), name='report'),
]