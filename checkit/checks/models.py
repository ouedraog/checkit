from django.contrib.auth.models import User
from django.db import models
from django.utils.html import escape
from django.utils.translation import ugettext_lazy as _

import bleach

from checkit.activities.models import Activity


class CheckTag(models.Model):
    tag = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Check Tag'
        verbose_name_plural = 'Check Tags'
        
    def __unicode__(self):
        return self.tag
    
class Check(models.Model):
    user = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True)
    post = models.TextField(max_length=255)
    parent = models.ForeignKey('Check', null=True, blank=True)
    likes = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)
    picture = models.ImageField(upload_to='check_images', blank=True, null= True)
    longitude = models.FloatField(default=0)
    latitude = models.FloatField(default=0)
    all_of_fame = models.BooleanField()
    visibility = models.BooleanField()
    tags = models.ManyToManyField(CheckTag, related_name='tags', symmetrical=True, null=True, blank=True)

    class Meta:
        verbose_name = _('Check')
        verbose_name_plural = _('Checks')
        ordering = ('-date',)

    def __unicode__(self):
        return self.post

    @staticmethod
    def get_checks(from_check=None):
        if from_check is not None:
            checks = Check.objects.filter(parent=None, id__lte=from_check)
        else:
            checks = Check.objects.filter(parent=None)
        return checks

    @staticmethod
    def get_checks_after(Check):
        checks = Check.objects.filter(parent=None, id__gt=Check)
        return checks

    def get_comments(self):
        return Check.objects.filter(parent=self).order_by('date')

    def calculate_likes(self):
        likes = Activity.objects.filter(activity_type=Activity.LIKE, Check=self.pk).count()
        self.likes = likes
        self.save()
        return self.likes

    def get_likes(self):
        likes = Activity.objects.filter(activity_type=Activity.LIKE, Check=self.pk)
        return likes

    def get_likers(self):
        likes = self.get_likes()
        likers = []
        for like in likes:
            likers.append(like.user)
        return likers

    def calculate_comments(self):
        self.comments = Check.objects.filter(parent=self).count()
        self.save()
        return self.comments

    def comment(self, user, post):
        Check_comment = Check(user=user, post=post, parent=self)
        Check_comment.save()
        self.comments = Check.objects.filter(parent=self).count()
        self.save()
        return Check_comment

    def linkfy_post(self):
        return bleach.linkify(escape(self.post))
