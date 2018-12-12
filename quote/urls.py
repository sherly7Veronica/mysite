from django.conf.urls import url

from quote.views import QuoteListView, QuoteListCreateView, QuoteRUDView

urlpatterns = [
    url(r'^quote/$', QuoteListView.as_view(), name='quote'),
    url(r'^quote/list/$', QuoteListCreateView.as_view(), name='create'),
    url(r'^quote/detail/$', QuoteRUDView.as_view(), name='RUD'),
]