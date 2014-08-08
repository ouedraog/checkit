from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from checkit.api2 import views

urlpatterns = patterns('',
    url(r'^feeds/$', views.FeedList.as_view()),
    url(r'^feed/(?P<pk>[0-9]+)/$', views.FeedDetail.as_view()),
)

urlpatterns = format_suffix_patterns(urlpatterns)