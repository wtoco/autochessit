from networktools.common import views
from django.conf.urls import url

urlpatterns = [
    url(r'^common_catalogue/', views.common_catalogue, name='common_catalogue'),
    url(r'^tcp_easy_test/', views.tcp_easy_test, name='tcp_easy_test'),
    url(r'^udp_easy_test/', views.udp_easy_test, name='udp_easy_test'),
    url(r'^tcp_group_test/', views.tcp_group_test, name='tcp_group_test'),
    url(r'^udp_group_test/', views.udp_group_test, name='udp_group_test'),
    url(r'^ping_tracrt_to_file/', views.ping_tracrt_to_file, name='ping_tracrt_to_file'),
]
