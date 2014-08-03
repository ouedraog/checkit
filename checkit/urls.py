from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^grappelli/', include('grappelli.urls')),  # grappelli URLS
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'checkit.core.views.home', name='home'),
    url(r'^login', 'django.contrib.auth.views.login', {'template_name': 'core/cover.html'}, name='login'),
    url(r'^logout', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
    url(r'^signup/$', 'checkit.auth.views.signup', name='signup'),
    url(r'^settings/$', 'checkit.core.views.settings', name='settings'),
    url(r'^settings/picture/$', 'checkit.core.views.picture', name='picture'),
    url(r'^settings/upload_picture/$', 'checkit.core.views.upload_picture', name='upload_picture'),
    url(r'^settings/save_uploaded_picture/$', 'checkit.core.views.save_uploaded_picture', name='save_uploaded_picture'),
    url(r'^settings/password/$', 'checkit.core.views.password', name='password'),
    url(r'^network/$', 'checkit.core.views.network', name='network'),
    url(r'^feeds/', include('checkit.feeds.urls')),
    url(r'^questions/', include('checkit.questions.urls')),
    url(r'^articles/', include('checkit.articles.urls')),
    url(r'^messages/', include('checkit.messages.urls')),
    url(r'^notifications/$', 'checkit.activities.views.notifications', name='notifications'),
    url(r'^notifications/last/$', 'checkit.activities.views.last_notifications', name='last_notifications'),
    url(r'^notifications/check/$', 'checkit.activities.views.check_notifications', name='check_notifications'),
    url(r'^search/$', 'checkit.search.views.search', name='search'),
    url(r'^(?P<username>[^/]+)/$', 'checkit.core.views.profile', name='profile'),
    url(r'^i18n/', include('django.conf.urls.i18n', namespace='i18n')),
    url(r'^search2/', include('haystack.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
