from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^auth/', include('loginsys.urls')),
    url(r'', include('horserace.urls')),
    url(r'^i18n/', include('django.conf.urls.i18n')),

]