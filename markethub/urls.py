from django.conf import  settings
from django.conf.urls.static import static
from django.contrib import admin
from django.conf.urls import url, include

urlpatterns = [

    url(r'',include('users.urls')),
    url(r'admin/',include('adminApp.urls'))
    #url('admin/', admin.site.urls),
]
if settings.DEBUG:
         urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
         urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)