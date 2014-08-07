from checkit.feeds.models import Feed, CheckTag
from checkit.auth.models import Profile
from django.contrib import admin
admin.site.register(Feed)
admin.site.register(CheckTag)
admin.site.register(Profile)