from django.db import transaction
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from . import models
import requests


class UserAPISerializer(ModelSerializer):
    """User's serializer for API"""
    class Meta:
        model = models.UserAPI
        fields = ("id","name","lastname","email","password",)
        extra_kwargs = {'password':{'write_only':True}}

    def create(self, data):
        """Create new user from API"""

        user = models.UserAPI(
            email = data['email'],
            name = data['name'],
            lastname = data['lastname']
        )
        user.set_password(data['password'])
        user.save()
        return user

class UserAPISerializerUpdate(ModelSerializer):
    """Update fields for user for connect to etherscan.io"""

    class Meta:
        model = models.UserAPI
        fields = ("id","ether_address","api_key")
    
    
class UserProfileSerializer(ModelSerializer):

    class Meta:
        model = models.UserProfile
        fields = ('ether_address', 'ether_api_key')


class UserSerializer(ModelSerializer):
    profile = UserProfileSerializer()

    class Meta:
        model = models.UserAPI
        fields = ('id', 'email', 'name', 'lastname', 'profile')
        extra_kwargs = {
            'email': {'read_only': True}
        }

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name')
        instance.lastname = validated_data.get('lastname')
        profile = validated_data.get('profile')
        instance.profile.ether_address = profile.get('ether_address')
        instance.profile.ether_api_key = profile.get('ether_api_key')
        with transaction.atomic():
            instance.save(update_fields=['name', 'lastname'])
            instance.profile.save(update_fields=['ether_address', 'ether_api_key'])
        return instance


class UserEtherSerializer(ModelSerializer):
    ether_address = serializers.CharField(source='profile.ether_address', read_only=True)
    ether_info = serializers.SerializerMethodField(source='get_ether_info')
    ''' Альтернатива '''
    # balance = serializers.SerializerMethodField(source='get_balance')
    # last_block = serializers.SerializerMethodField(source='get_last_block')
    # ether_price = serializers.SerializerMethodField(source='get_ether_price')

    class Meta:
        model = models.UserAPI
        fields = ('ether_address', 'ether_info')
        ''' Альтернатива '''
        # fields = ('ether_address', 'balance', 'last_block', 'ether_price')
    ''' Альтернатива '''
    # def get_balance(self, obj):
    #     url = 'https://api.etherscan.io/api?module=account&action=balance&address={0}&tag=latest&apikey={1}'
    #     response = requests.get(url.format(obj.profile.ether_address, obj.profile.ether_api_key))
    #     if response.status_code == 200:
    #         return response.json()
    #     return None
    #
    # def get_last_block(self, obj):
    #     url = 'https://api.etherscan.io/api?module=proxy&action=eth_blockNumber&apikey={0}'
    #     response = requests.get(url.format(obj.profile.ether_api_key))
    #     if response.status_code == 200:
    #         return response.json()
    #     return None
    #
    # def get_ether_price(self, obj):
    #     url = 'https://api.etherscan.io/api?module=stats&action=ethprice&apikey={0}'
    #     response = requests.get(url.format(obj.profile.ether_api_key))
    #     if response.status_code == 200:
    #         return response.json()
    #     return None

    def get_ether_info(self, obj):
        # balance
        url = 'https://api.etherscan.io/api?module=account&action=balance&address={0}&tag=latest&apikey={1}'
        response = requests.get(url.format(obj.profile.ether_address, obj.profile.ether_api_key))
        balance = None
        if response.status_code == 200:
            balance = response.json()

        # last block
        url = 'https://api.etherscan.io/api?module=proxy&action=eth_blockNumber&apikey={0}'
        response = requests.get(url.format(obj.profile.ether_api_key))
        last_block = None
        if response.status_code == 200:
            last_block = response.json()

        # ether_price
        url = 'https://api.etherscan.io/api?module=stats&action=ethprice&apikey={0}'
        response = requests.get(url.format(obj.profile.ether_api_key))
        ether_price = None
        if response.status_code == 200:
            ether_price = response.json()

        result = {
            'balance': balance,
            'las_block': last_block,
            'ether_price': ether_price
        }
        return result
