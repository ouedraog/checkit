from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from checkit.api3 import views
from django.contrib.auth.models import User

urlpatterns = patterns('',
                       
    url(r'^users/$', views.UserList.as_view()),
    url(r'^user/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
    
    url(r'^profiles/$', views.ProfileList.as_view()),
    url(r'^profile/(?P<pk>[0-9]+)/$', views.ProfileDetail.as_view()),
    
    url(r'^feeds/$', views.FeedList.as_view(model=User), name='feeds-list'),
    url(r'^followees_feeds/$', views.FolloweesFeedList.as_view()),
    url(r'^feed/(?P<pk>[0-9]+)/$', views.FeedDetail.as_view()),
    
    url(r'^activities/$', views.ActivityList.as_view()),
    url(r'^activity/(?P<pk>[0-9]+)/$', views.ActivityDetail.as_view()),
    
    url(r'^tags/$', views.TagList.as_view()),
    url(r'^tag/(?P<pk>[0-9]+)/$', views.TagDetail.as_view()),
    
    url(r'^notifications/$', views.NotificationList.as_view()),
    url(r'^mynotifications/$', views.MyNotificationList.as_view()),
    url(r'^notification/(?P<pk>[0-9]+)/$', views.NotificationDetail.as_view()),
    url(r'^api-login/', views.api_login),
)

urlpatterns = format_suffix_patterns(urlpatterns)