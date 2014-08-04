import datetime
from haystack import indexes
from checkit.feeds.models import Feed

from django.db import models
from django.contrib.auth.models import User


class FeedIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=False )
    post = indexes.CharField(model_attr='post')
    longitude= indexes.FloatField(model_attr='longitude')
    latitude= indexes.FloatField(model_attr='latitude')
    date=indexes.DateTimeField(model_attr='date')
    tags = indexes.MultiValueField( null=True)

    def get_model(self):
        return Feed

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(date__lte=datetime.datetime.now())
    
    def prepare_tags(self, obj):
        return [tag.tag for tag in obj.tags.all()]
    