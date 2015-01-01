from django.conf.urls import patterns, include, url

from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include
from django.contrib.auth.models import User
from rest_framework import serializers, viewsets, routers
from django.conf.urls import url
from signups import views
from signups.views import IncetiveViewSet
from rest_framework import renderers
from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import include
from django.contrib import admin
admin.autodiscover()

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
incentive_list = IncetiveViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
incentive_detail = IncetiveViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
incentive = IncetiveViewSet.as_view({
    'get': 'highlight'
}, renderer_classes=[renderers.StaticHTMLRenderer])
user_list = UserViewSet.as_view({
    'get': 'list'
})
user_detail = UserViewSet.as_view({
    'get': 'retrieve'
})


# Routers provide a way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'incentive', views.IncetiveViewSet)
router.register(r'users', UserViewSet)
#urlpatterns = patterns('',
#    # Examples:
#   url(r'^$', 'signups.views.home', name='home'),
#    # url(r'^blog/', include('blog.urls')),
#    url(r'^thank-you/$', 'signups.views.thankyou', name='thankyou'),
#    url(r'^about-us/$', 'signups.views.aboutus', name='aboutus'),
#    url(r'^users/$', views.UserList.as_view()),
#    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
#    #url(r'^Json/$', 'signups.views.json', name='json'),
#    #url(r'^incetive/$', views.incetive_list,name='incetive-list'),
#    #url(r'^invetive/(?P<pk>[0-9]+)/$', views.incetive_detail,name='incetive-detail'),
#    url(r'^incentives/$', views.IncentiveList.as_view()),
#    url(r'^incetnives/(?P<pk>[0-9]+)/$', views.IncentiveDetail.as_view()),
#    url(r'^admin/', include(admin.site.urls)),
#    url(r'^', include(router.urls)),
#    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
#    url(r'^$', views.api_root),
#    url(r'^incentive/(?P<pk>[0-9]+)/highlight/$', views.IncentiveHighlight.as_view()),
#)
#
#
#urlpatterns = format_suffix_patterns(urlpatterns)

## API endpoints
#urlpatterns = format_suffix_patterns([
#    url(r'^$', views.api_root),
#    url(r'^incentive/$',
#        views.IncentiveList.as_view(),
#        name='incentive-list'),
#    url(r'^snippets/(?P<pk>[0-9]+)/$',
#        views.IncentiveDetail.as_view(),
#        name='incentive-detail'),
#    url(r'^snippets/(?P<pk>[0-9]+)/highlight/$',
#        views.IncentiveHighlight.as_view(),
#        name='incentive-highlight'),
#    url(r'^users/$',
#        views.UserList.as_view(),
#        name='user-list'),
#    url(r'^users/(?P<pk>[0-9]+)/$',
#        views.UserDetail.as_view(),
#        name='user-detail')
#])

#urlpatterns = format_suffix_patterns([
#    url(r'^$', api_root),
#    url(r'^incentive/$', incentive_list, name='incentive-list'),
#    url(r'^incentive/(?P<pk>[0-9]+)/$', incentive_detail, name='incentive-detail'),
#    url(r'^incentive/(?P<pk>[0-9]+)/highlight/$', incentive_highlight, name='incentive-highlight'),
#    url(r'^users/$', user_list, name='user-list'),
#    url(r'^users/(?P<pk>[0-9]+)/$', user_detail, name='user-detail')
#])

# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.
urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^about/$', views.about),
    url(r'^test/$', views.incentiveTest),
    url(r'^xml/$', views.xml),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^$', 'signups.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^add/','signups.views.addIncentive',name='add')
   # url(r'^thank-you/$', 'signups.views.thankyou', name='thankyou'),
   # url(r'^about-us/$', 'signups.views.aboutus', name='aboutus'),

]

## Login and logout views for the browsable API
#urlpatterns += [
#    url(r'^api-auth/', include('rest_framework.urls',
#                               namespace='rest_framework')),
#]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

    