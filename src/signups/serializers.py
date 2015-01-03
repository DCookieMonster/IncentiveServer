from django.contrib.auth.models import User, Group
from django.forms import widgets
from rest_framework import serializers
from signups.models import Incentive,Tag
import urllib2,os,json,xmltodict

class UserSerializer(serializers.HyperlinkedModelSerializer):
    incentive = serializers.HyperlinkedRelatedField(many=True, view_name='incentive-detail', read_only=True)

    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'incentive')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('tagID', 'tagName')

# class IncentiveSerializer(serializers.ModelSerializer):
#     tags=TagSerializer(many=True, read_only=True)
#     class Meta:
#         model = Incentive
#         fields = ('schemeName', 'schemeID','text','typeID','typeName','status','ordinal','tags','modeID',
#         'groupIncentive','condition')

class IncentiveSerializer(serializers.ModelSerializer):
    tags=TagSerializer(many=True,  read_only=False)

    class Meta:
        model = Incentive
        fields = ('schemeName', 'schemeID','text','typeID','typeName','status','ordinal','tags','modeID',
        'groupIncentive','condition')

    def create(self, validated_data):
        f=open('myfile', 'w')
        tags_data = validated_data.pop('tags',[])
        f.write(json.dumps(tags_data,indent=4))
        f.close()
        incentive = super(IncentiveSerializer, self).create(validated_data)
        for tag in tags_data:
            if tag is not None:
                #Tag.objects.create(incentiveID=incentive,**tag)
                Tag.objects.create(**tag)

        # Ignores tags without a tagId
        #tags_ids = [tag["incentiveID"] for tag in tags_data if "incentiveID" in tag]
        tags_ids = [tag["tagID"] for tag in tags_data if "tagID" in tag]
        f1=open('tagsID','w')
        f1.write(json.dumps(tags_ids,indent=4))
        f1.close()
        if tags_ids:
            tags = Tag.objects.filter(tagID__in=tags_ids)
            incentive.tags.add(*tags)


        return incentive