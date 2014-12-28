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



#class IncentiveSerializer(serializers.Serializer):
#    pk = serializers.IntegerField(read_only=True)
#    owner = serializers.ReadOnlyField(source='owner.username')
#    title = serializers.CharField(required=False, allow_blank=True, max_length=100)
#    code = serializers.CharField(style={'type': 'textarea'})
#    Email = serializers.EmailField()
#    
#
#    def create(self, validated_data):
#        """
#        Create and return a new `Snippet` instance, given the validated data.
#        """
#        return Incentive.objects.create(**validated_data)
#
#    def update(self, instance, validated_data):
#        """
#        Update and return an existing `Snippet` instance, given the validated data.
#        """
#        instance.title = validated_data.get('title', instance.title)
#        instance.code = validated_data.get('code', instance.code)
#        instance.Email = validated_data.get('Email', instance.Email)
#        instance.save()
#        return instance
    
class IncentiveSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField(view_name='incentive-highlight', format='html')

    class Meta:
        model = Incentive
        fields = ('url', 'highlight', 'owner',
                  'title', 'code','email')
    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Incentive.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.code = validated_data.get('code', instance.code)
        instance.Email = validated_data.get('Email', instance.Email)
        instance.save()
        return instance