
from django.conf.urls import url
from . import views

app_name = 'chengdu'
urlpatterns = [
    url(r'^add_mac_file/', views.add_mac_file, name='add_mac_file'),
    url(r'^add_mac/', views.add_mac, name='add_mac'),
    url(r'^chengdu_catalogue/', views.chengdu_catalogue, name='chengdu_catalogue'),
]
