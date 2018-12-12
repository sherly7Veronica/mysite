from django.conf.urls import url
from hubs.views import HubListView, HubListCreateView, HubRUDView

urlpatterns = [
    url(r'^hubs/$', HubListView.as_view(), name='quote'),
    url(r'^hubs/list/$', HubListCreateView.as_view(), name='create'),
    url(r'^hubs/detail/$', HubRUDView.as_view(), name='RUD'),
]