import datetime
from haystack import indexes
from checkit.feeds.models import Feed

from django.db import models
from django.contrib.auth.models import User


class Note(models.Model):
    user = models.ForeignKey(User)
    pub_date = models.DateTimeField()
    title = models.CharField(max_length=200)
    body = models.TextField()

    def __unicode__(self):
        return self.title

class NoteIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    author = indexes.CharField(model_attr='user')
    pub_date = indexes.DateTimeField(model_attr='pub_date')

    def get_model(self):
        return Note

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(pub_date__lte=datetime.datetime.now())
    

class FeedIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=False)
    post = indexes.CharField(model_attr='post')
    longitude= indexes.FloatField(model_attr='longitude')
    latitude= indexes.FloatField(model_attr='latitude')
    date=indexes.DateTimeField(model_attr='date')

    def get_model(self):
        return Feed

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(date__lte=datetime.datetime.now())
    