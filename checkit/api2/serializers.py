from rest_framework import serializers

class UserSerializer(serializers.Serializer):
    id=serializers.IntegerField()
    username=serializers.CharField(max_length=100)
    email=serializers.EmailField()
    first_name=serializers.CharField(max_length=100)
    last_name=serializers.CharField(max_length=100)
    
class ProfileSerializer(serializers.Serializer):
    id=serializers.IntegerField()
    user=serializers.RelatedField()
    job_title=serializers.CharField(max_length=50)
    tel = serializers.CharField(max_length=50)
    location = serializers.CharField(max_length=50)
    sex=serializers.CharField(max_length=2)
    birthday=serializers.DateField()
    photo=serializers.ImageField()
    followees=serializers.ManyRelatedField()
 
    
class FeedSerializer(serializers.Serializer):
    id=serializers.IntegerField()
    user = serializers.RelatedField()
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
    
class ActivitySerializer(serializers.Serializer):
    id=serializers.IntegerField()
    user = serializers.RelatedField()
    activity_type = serializers.CharField()
    date = serializers.DateTimeField()
    feed = serializers.IntegerField()
    
class NotificationSerializer(serializers.Serializer):
    id=serializers.IntegerField()
    from_user=serializers.RelatedField()
    to_user = serializers.RelatedField()
    date = serializers.DateTimeField()
    feed = serializers.RelatedField()
    notification_type = serializers.CharField()
    is_read = serializers.BooleanField()
    