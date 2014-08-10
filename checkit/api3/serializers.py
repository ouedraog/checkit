from rest_framework import serializers
from checkit.feeds.models import Feed, CheckTag
from django.contrib.auth.models import User
from checkit.auth.models import Profile
from checkit.activities.models import Notification, Activity
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        write_only_fields = ['password']
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Profile
 
    
class FeedSerializer(serializers.ModelSerializer):
    class Meta:
        model=Feed
    
class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model=Activity
    
class NotificationSerializer(serializers.Serializer):
    class Meta:
        model=Notification
        
class CheckTagSerializer(serializers.ModelSerializer):
    class Meta:
        model=CheckTag
        
    