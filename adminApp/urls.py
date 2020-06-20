from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^login/$',views.login, name = 'adminLoginPage'),
    url(r'^home/$',views.homepage, name = 'adminHomePage'),
    url(r'^allUploads/$', views.allUploads, name = 'adminAllUploadsPage'),
    url(r'^allUploads/(?P<itemId>[\d]+)/$', views.itemDetails, name = 'adminItemDetailsPage'),
    url(r'^reports/$', views.allChats, name = 'reportsPage'),
    url(r'^allUsers/$', views.allUsers, name="allUsersPage"),
    url(r'^allUsers/(?P<userId>[\d]+)/suspend/$', views.suspendUser, name="suspendUsersPage"),
    url(r'^allUsers/suspended/$', views.allSuspendedUser, name="allSuspendedUserPage"),
    url(r'^allUsers/(?P<userId>[\d]+)/restore/$', views.restoreUser, name="restoreUserPage"),
    url(r'^reports/(?P<chatId>[\d]+)/$', views.chat, name = 'adminChatPage')
    ]
