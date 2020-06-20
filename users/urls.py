from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.home, name = 'startPage'),
    url(r'^signUp/$',views.signUp, name = 'signUpPage'),
    url(r'^login/$',views.login, name = 'loginPage'),
    url(r'^hub/$',views.hubHome, name = 'hubPage'),
    url(r'^hub/item/(?P<itemId>[\d]+)/$',views.itemDetails, name = 'itemDetailPage'),
    url(r'^hub/chat/(?P<chatId>[\d]+)/$',views.chat, name = 'chatPage'),
    url(r'^hub/upload/$',views.upload, name = 'uploadPage'),
    url(r'^hub/allUpload/$',views.viewAllUploads, name = 'allUploadsPage'),
    url(r'^hub/allUpload/(?P<itemId>[\d]+)/$',views.individualItem, name = 'individualItemPage'),
    url(r'^hub/allUpload/(?P<itemId>[\d]+)/edit/$',views.updateItem, name = 'editItemPage'),
    url(r'^hub/allUpload/(?P<itemId>[\d]+)/delete/$',views.deleteItem, name = 'deleteItemPage'),
    url(r'^hub/messages/$', views.allChats, name='messagesPage'),
    url(r'^hub/profile/$', views.profile, name='profilePage'),
    url(r'^hub/profile/edit/$', views.editProfile, name='editProfilePage'),
    url(r'hub/report/$', views.report, name ='reportPage'),
    url(r'^hub/logout/$',views.logout, name = 'logoutPage'),

]