from checkit.feeds.models import Feed
from django.contrib.auth.models import User
from checkit.auth.models import Profile

from .serializers import FeedSerializer
from .serializers import UserSerializer

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response

class UserList(APIView):
    
    def get(self, request, format=None):
        users = User.objects.all()
        serialized_users = UserSerializer(users, many=True)
        return Response(serialized_users.data)
    
class UserDetail(APIView):
    
    def get_object(self, pk):
        
        try:
            return User.objects.get(pk=pk)
        
        except: User.DoesNotExist
        raise Http404
    
    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serialized_user = UserSerializer(user)
        return Response(serialized_user.data)
            

class FeedList(APIView):
    
    def get(self, request, format=None):
        feeds = Feed.objects.all()
        serialized_feeds = FeedSerializer(feeds, many=True)
        return Response(serialized_feeds.data)
    
class FeedList_Follower(APIView):
    
    def get(self, request, format=None):
        p=Profile.objects.get(user=request.user)
        feeds = Feed.objects.filter(user =p.followees.all())
        serialized_feeds = FeedSerializer(feeds, many=True)
        return Response(serialized_feeds.data)

class FeedDetail(APIView):
    
    def get_object(self, pk):
        
        try:
            return Feed.objects.get(pk=pk)
        
        except: Feed.DoesNotExist
        raise Http404
    
    def get(self, request, pk, format=None):
        feed = self.get_object(pk)
        serialized_feed = FeedSerializer(feed)
        return Response(serialized_feed.data)
        
        
            
 
