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

admin.site.site_header = 'Incentive Server'
admin.site.site_title = 'Incentive Server'
admin.site.index_title = 'Admin'
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

urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^about/$', views.about),
    url(r'^test/$', views.incentiveTest),
    url(r'^xml/$', views.xml),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^$', 'signups.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^add/','signups.views.addIncentive',name='add'),
    url(r'^users/$', views.UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
    url(r'^incentives/$', views.incetive_list,name='incentives'),
    url(r'^login/$', views.login,name='login'),
    url(r'^wiki/', views.wiki,name='wiki'),
    url(r'^aboutus/', views.aboutus,name='aboutus'),
    url(r'^list/$', 'signups.views.list', name='data_set'),
    url(r'^profile/', 'signups.views.userProfile', name='profile_page'),
    url(r'^startAlg/', 'signups.runner.startAlg', name='startAlg'),
    url(r'^getInc/', 'signups.runner.getRatedIncentives', name='getInc'),
    url(r'^getIncUser/$', 'signups.views.getUserID', name='getIncUser'),


]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

