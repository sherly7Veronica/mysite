from django.conf.urls import url

from .views import QuestionListView, QuestionListCreateView, QuestionView, ChoiceListView, \
    ChoiceListCreateView, ChoiceListRUDView, ChoiceView, QuestionListRUDView

urlpatterns = [
    url(r'^question/$', QuestionListView().as_view(), name='list'),
    url(r'^question/create/$', QuestionListCreateView.as_view(), name='create'),
    url(r'^question/(?P<pk>\d+)/$', QuestionListRUDView.as_view(), name='RUD'),
    url(r'^question/view/$', QuestionView.as_view(), name='api-view'),
    url(r'^choice/$', ChoiceListView.as_view(), name='choice-list'),
    url(r'^choice/create/$', ChoiceListCreateView.as_view(), name='choice-create'),
    url(r'^choice/(?P<pk>\d+)/$', ChoiceListRUDView.as_view(), name='choice-RUD'),
    url(r'^choice/view/$', ChoiceView.as_view(), name='choice-view')
]
