from django.contrib.auth.models import User, Group
from django.forms import widgets
from rest_framework import serializers
from signups.models import Incentive


class UserSerializer(serializers.HyperlinkedModelSerializer):
    incentive = serializers.HyperlinkedRelatedField(many=True, view_name='incentive-detail', read_only=True)

    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'incentive')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class IncentiveSerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    owner = serializers.ReadOnlyField(source='owner.username')
    schemeID = serializers.IntegerField(required=True)
    schemeName = serializers.CharField()
    text =  serializers.CharField(style={'type': 'textarea'})
    typeID=serializers.IntegerField(required=True)
    typeName=serializers.CharField()
    status=serializers.BooleanField(required=True)
    ordinal=serializers.IntegerField(required=False)
    modeID=serializers.IntegerField(required=False)
    groupIncentive=serializers.BooleanField(required=False)
    condition=serializers.CharField(style={'type': 'textarea'})

    def create(self, validated_data):
        """
       Create and return a new `Incentive` instance, given the validated data.
       """
        return Incentive.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
       Update and return an existing `Incentive` instance, given the validated data.
       """
        instance.schemeName = validated_data.get('schemeName', instance.schemeName)
        instance.schemeID = validated_data.get('schemeID', instance.schemeID)
        instance.text = validated_data.get('text', instance.text)
        instance.typeID=validated_data.get('typeID',instance.typeID)
        instance.typeName=validated_data.get('typeName',instance.typeName)
        instance.status=validated_data.get('status',instance.status)
        instance.ordinal=validated_data.get('ordinal',instance.ordinal)
        instance.modeID=validated_data.get('modeID',instance.modeID)
        instance.groupIncentive=validated_data.get('groupIncentive',instance.groupIncentive)
        instance.condition=validated_data.get('condition',instance.condition)




        instance.save()
        return instance


# class IncentiveSerializer(serializers.HyperlinkedModelSerializer):
#     owner = serializers.ReadOnlyField(source='owner.username')
#     highlight = serializers.HyperlinkedIdentityField(view_name='incentive-highlight', format='html')
#
#     class Meta:
#         model = Incentive
#         fields = ('url', 'highlight', 'owner',
#                   'id', 'schemeName', 'text')
#
#     def create(self, validated_data):
#         """
#         Create and return a new `Incentive` instance, given the validated data.
#         """
#         return Incentive.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         """
#         Update and return an existing `Incentive` instance, given the validated data.
#         """
#
#         instance.title = validated_data.get('title', instance.title)
#         instance.code = validated_data.get('code', instance.code)
#         instance.Email = validated_data.get('Email', instance.Email)
#         instance.save()
#         return instance