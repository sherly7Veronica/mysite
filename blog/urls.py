from django.conf.urls import url
# from django.urls import path
from .views import BlogListView


urlpatterns = [
    url('^blog/list/$', BlogListView.as_view())
]