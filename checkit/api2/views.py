from checkit.feeds.models import Feed
from checkit.api2.serializers import FeedSerializer
from rest_framework import generics


class FeedList(generics.ListCreateAPIView):
    queryset = Feed.objects.all()
    serializer_class = FeedSerializer

    
class FeedDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Feed.objects.all()
    serializer_class = FeedSerializer
    