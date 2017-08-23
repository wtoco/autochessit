from django.conf.urls import url, include
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^networktools/common/', include('networktools.common.urls')),
    url(r'^networktools/custom/chengdu/', include('networktools.custom.chengdu.urls')),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^$', views.index, name='index'),
    url(r'^about/', views.about, name='about'),
]
