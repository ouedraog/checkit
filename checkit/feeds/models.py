from django.contrib.auth.models import User
from django.db import models
from django.utils.html import escape
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save, m2m_changed

import bleach

from checkit.activities.models import Activity
from django.forms.fields import NullBooleanField
from django.utils import timezone

class CheckTag(models.Model):
    tag = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Check Tag'
        verbose_name_plural = 'Check Tags'
        
    def __unicode__(self):
        return self.tag
    
class Feed(models.Model):
    user = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True)
    post = models.TextField(max_length=255)
    parent = models.ForeignKey('Feed', null=True, blank=True)
    likes = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)
    picture = models.ImageField(upload_to='check_images',  null=True, blank=True)
    longitude = models.FloatField(default=0)
    latitude = models.FloatField(default=0)
    all_of_fame = models.BooleanField(default=False)
    visibility = models.BooleanField(default=False)
    staff_pick=models.BooleanField(default=False)
    tags = models.ManyToManyField(CheckTag,  null=True, blank=True)

    class Meta:
        verbose_name = _('Feed')
        verbose_name_plural = _('Feeds')
        ordering = ('-date',)

    def __unicode__(self):
        return self.post

    @staticmethod
    def get_feeds(from_feed=None):
        if from_feed is not None:
            feeds = Feed.objects.filter(parent=None, id__lte=from_feed)
        else:
            feeds = Feed.objects.filter(parent=None)
        return feeds

    @staticmethod
    def get_feeds_after(feed):
        feeds = Feed.objects.filter(parent=None, id__gt=feed)
        return feeds

    def get_comments(self):
        return Feed.objects.filter(parent=self).order_by('date')

    def calculate_likes(self):
        likes = Activity.objects.filter(activity_type=Activity.LIKE, feed=self.pk).count()
        self.likes = likes
        self.save()
        return self.likes

    def get_likes(self):
        likes = Activity.objects.filter(activity_type=Activity.LIKE, feed=self.pk)
        return likes

    def get_likers(self):
        likes = self.get_likes()
        likers = []
        for like in likes:
            likers.append(like.user)
        return likers

    def calculate_comments(self):
        self.comments = Feed.objects.filter(parent=self).count()
        self.save()
        return self.comments

    def comment(self, user, post):
        feed_comment = Feed(user=user, post=post, parent=self)
        feed_comment.save()
        self.comments = Feed.objects.filter(parent=self).count()
        self.save()
        return feed_comment

    def linkfy_post(self):
        return bleach.linkify(escape(self.post))
    