from checkit.feeds.models import Feed
from checkit.auth.models import Profile
from checkit.activities.models import Activity, Notification
from django.contrib.auth.models import User

from checkit.api3.serializers import *
from rest_framework import generics

from django.http import Http404, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login


def api_login(request):
    username = request.GET['username']
    password = request.GET.get("password")
    user = authenticate(username=username, password=password)
    login(request, user)
    if not request.GET.has_key('remember_me'): 
        request.session.set_expiry(0)
    return HttpResponse(user.is_authenticated())
    
class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def pre_save(self, obj):
        obj.password = make_password(obj.password)

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
class ProfileList(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class FeedList(generics.ListCreateAPIView):
    queryset = Feed.objects.all()
    serializer_class = FeedSerializer
    
    
class FeedDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Feed.objects.all()
    serializer_class = FeedSerializer

class FolloweesFeedList(APIView):
    def get(self, request, format=None):
        p=Profile.objects.get(user=request.user)
        feeds = Feed.objects.filter(user =p.followees.all())
        serialized_feeds = FeedSerializer(feeds, many=True)
        return Response(serialized_feeds.data)
    
class ActivityList(generics.ListCreateAPIView):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    
class ActivityDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    
class NotificationList(generics.ListCreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    
class MyNotificationList(APIView):
    def get(self, request, format=None):
        notifications = Notification.objects.filter(to_user =request.user)
        serialized_notifications = NotificationSerializer(notifications, many=True)
        return Response(serialized_notifications.data)
    
class NotificationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

class TagList(generics.ListCreateAPIView):
    queryset = CheckTag.objects.all()
    serializer_class = CheckTagSerializer
      
class TagDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CheckTag.objects.all()
    serializer_class = CheckTagSerializer