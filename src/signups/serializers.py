from django.contrib.auth.models import User, Group
from django.forms import widgets
from rest_framework import serializers
from signups.models import Incentive,Tag
import urllib2,os,json,xmltodict

# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     incentive = serializers.HyperlinkedRelatedField(many=True, view_name='incentive-detail', read_only=True)
#
#     class Meta:
#         model = User
#         fields = ('url', 'username', 'email', 'incentive')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('tagID', 'tagName')


from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    incentive = serializers.PrimaryKeyRelatedField(many=True, queryset=Incentive.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'incentive')

import logging
logger = logging.getLogger(__name__)

class IncentiveSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True,  read_only=False)
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Incentive
        fields = ('owner','schemeName', 'schemeID','text','typeID','typeName','status','ordinal','tags','modeID',
        'groupIncentive','condition')

    def create(self, validated_data):
     #   logger.info(validated_data)
        tags_data = validated_data.pop('tags',[])
        incentive = super(IncentiveSerializer, self).create(validated_data)
        for tag in tags_data:
            if tag is not None:
                tags_ids = [tag["tagID"] for tag in tags_data if "tagID" in tag]
                if tags_ids is None:
                    #Tag.objects.create(incentiveID=incentive,**tag)
                    Tag.objects.create(**tag)

        # Ignores tags without a tagId
        #tags_ids = [tag["incentiveID"] for tag in tags_data if "incentiveID" in tag]
        tags_ids = [tag["tagID"] for tag in tags_data if "tagID" in tag]

        if tags_ids:
            tags = Tag.objects.filter(tagID__in=tags_ids)
            incentive.tags.add(*tags)

        logger.info("added new incentive:"+str(incentive))

        return incentive