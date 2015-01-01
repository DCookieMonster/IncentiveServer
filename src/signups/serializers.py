from django.contrib.auth.models import User, Group
from django.forms import widgets
from rest_framework import serializers
from signups.models import Incentive,Tag


class UserSerializer(serializers.HyperlinkedModelSerializer):
    incentive = serializers.HyperlinkedRelatedField(many=True, view_name='incentive-detail', read_only=True)

    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'incentive')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

class TagSerializer(serializers.Serializer):
    class Meta:
        model = Tag
        fields = ('tagID', 'tagName')

class IncentiveSerializer(serializers.ModelSerializer):
    tags=TagSerializer(many=True, read_only=True)
    class Meta:
        model = Incentive
        fields = ('schemeName', 'schemeID','text','typeID','typeName','status','ordinal','tags','modeID',
        'groupIncentive','condition')

