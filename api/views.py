from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import permissions

from rest_framework import viewsets
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from . import models
from . import serializers
import requests
import json


class UserAPIView(viewsets.ModelViewSet):
    
    """
    Add new user with lastname and email
    """
    
    serializer_class = serializers.UserAPISerializer
    queryset = models.UserAPI.objects.all()


class LoginViewSet(viewsets.ViewSet):
    
    """Get token from name and password post for auth"""

    serializer_class = AuthTokenSerializer

    def create(self, request):
        return ObtainAuthToken().post(request)

class UpdateEtherSet(viewsets.ModelViewSet):
    
    """Add fields for getting information from etherscan.io - ethereum address and api kay"""
    
    serializer_class = serializers.UserAPISerializerUpdate

    def get_queryset(self):
        current_id = self.kwargs['id']
        print('test of id',current_id)
        result = models.UserAPI.objects.all().filter(id=current_id)
        print(result.values())
        return models.UserAPI.objects.all().filter(id=current_id)
    
    def create(self, request, id):
        current = models.UserAPI.objects.get(id=id)
        ether_address = request.data['ether_address']
        current.ether_address = ether_address
        api_key = request.data['api_key']
        current.api_key = api_key
        current.save()
        return Response({'api_key':api_key,'ether_address':ether_address })

class GetInfoFromEtherscan(viewsets.ModelViewSet):
    """
    Get information from etherscan.io
    balance
    current rate ether to USD, timestamp of this rate and so on
    last block of ethereum main net
    """
    
    serializer_class = serializers.UserAPISerializerUpdate

    def get_queryset(self):
        current_id = self.kwargs['id']
        print('test of id',current_id)
        result = models.UserAPI.objects.all().filter(id=current_id)
        print(result.values())
        return models.UserAPI.objects.all().filter(id=current_id)

    def create(self, request, id):
        
        current = models.UserAPI.objects.all().filter(id=id)
        print('test of current',current.values('api_key','ether_address'))
        for item in current.values('api_key','ether_address'):
            api_key = item['api_key']
            ether_address = item['ether_address']
        #url_for_balance = 'https://api.etherscan.io/api?module=account&action=balance&address='+ether_address + \
        #'&tag=latest&apikey='+api_key
        get_balance = requests.get('https://api.etherscan.io/api?module=account&action=balance&address=%s&tag=latest&apikey=%s' % (ether_address,api_key)).json()['result']
        last_block = requests.get('https://api.etherscan.io/api?module=proxy&action=eth_blockNumber&apikey=%s' % (api_key)).json()['result']
        ether_price = requests.get('https://api.etherscan.io/api?module=stats&action=ethprice&apikey=%s' % (api_key)).json()['result']
        #get_balance = ''
        result = {"balance":get_balance,"last_block":last_block,"current_state":ether_price}
        
        return Response(result)

from rest_framework import generics, response
from rest_framework.permissions import IsAuthenticated


class UserView(generics.RetrieveUpdateAPIView):
    serializer_class = serializers.UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class UserEtherView(generics.RetrieveAPIView):
    serializer_class = serializers.UserEtherSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user
