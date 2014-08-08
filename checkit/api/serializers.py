from checkit.feeds.models import Feed
from rest_framework import serializers
from django.contrib.auth.models import User
from checkit.auth.models import Profile

    
class UserSerializer(serializers.Serializer):
    
    id=serializers.IntegerField()
    username=serializers.CharField(max_length=100)
    email=serializers.EmailField()
    first_name=serializers.CharField(max_length=100)
    last_name=serializers.CharField(max_length=100)
    tel = serializers.SerializerMethodField('get_tel')
    location = serializers.SerializerMethodField('get_location')
    sex=serializers.SerializerMethodField('get_sex')
    birthday=serializers.SerializerMethodField('get_birthday')
    photo=serializers.SerializerMethodField('get_photo')
    followees=serializers.SerializerMethodField('get_followers')

    
    def get_tel(self,obj):
        return Profile.objects.get(pk=obj.pk).tel

    def get_location(self,obj):
        return Profile.objects.get(pk=obj.pk).location
    
    def get_followers(self,obj):
        return Profile.objects.get(pk=obj.pk).followees.all()
    
    def get_sex(self,obj):
        return Profile.objects.get(pk=obj.pk).sex
    
    def get_birthday(self,obj):
        return Profile.objects.get(pk=obj.pk).birthday
    
    def get_photo(self,obj):
        return Profile.objects.get(pk=obj.pk).photo.url  
    
class FeedSerializer(serializers.Serializer):
    id=serializers.IntegerField()
    user = UserSerializer()
    date = serializers.DateTimeField()
    post = serializers.CharField()
    tags = serializers.ManyRelatedField()
    likes = serializers.IntegerField()
    picture = serializers.ImageField()
    longitude = serializers.FloatField()
    latitude = serializers.FloatField(default=0)
    all_of_fame = serializers.BooleanField(default=False)
    visibility = serializers.BooleanField(default=False)
    staff_pick=serializers.BooleanField(default=False)
    
