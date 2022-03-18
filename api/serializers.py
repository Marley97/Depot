from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.validators import UnicodeUsernameValidator
from .models import *
from django.db import transaction
from django.contrib.auth.models import Group
from rest_framework.response import Response
from django.contrib.auth.models import User


class TokenPairSerializer(TokenObtainPairSerializer):
	def validate(self, attrs):
		data = super(TokenPairSerializer, self).validate(attrs)
		data['groups'] = [group.name for group in self.user.groups.all()]
		data['username'] = self.user.username
		data['id'] = self.user.id
		data['first_name'] = self.user.first_name
		data['last_name'] = self.user.last_name
		return data

class GroupSerializer(serializers.ModelSerializer):

	class Meta:
		model = Group
		fields = "__all__"

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        read_only_fields = "is_active","is_staff"
        exclude = "last_login","is_staff","date_joined"

        extra_kwargs={
            'username':{
                'validators':[UnicodeUsernameValidator()]
            }
        } 
class DepotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Depot
        fields = "__all__"
        
class VendeurSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user']=UserSerializer(instance.user,many=False).data 
        user=UserSerializer(instance.user,many=False).data
        representation['user']={'id':user.get('id'),'username':user.get('user.username'),'first_name':user.get('user.first_name'),'last_name':user.get('user.last_name'),'password':user.get('user.password')}
        return representation   
        
    class Meta:
        model = Vendeur
        fields = "__all__"
        
class ProduitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produit
        fields = "__all__"
        
class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = "__all__"
        
class StockSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['produit']=ProduitSerializer(instance.produit,many=False).data 
        return representation 
    class Meta:
        model = Stock
        fields = "__all__"
        
class EmplacementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emplacement
        fields = "__all__"
        
class VenteSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user']=UserSerializer(instance.user,many=False).data 
        user=UserSerializer(instance.user,many=False).data
        representation['user']={'id':user.get('id'),'username':user.get('user.username')}
        representation['stock']=StockSerializer(instance.stock,many=False).data 
        stock=StockSerializer(instance.stock,many=False).data
        representation['stock']={'id':stock.get('id'),'produit':stock.get('produit')}
        representation['client']=ClientSerializer(instance.client,many=False).data 
        client=ClientSerializer(instance.client,many=False).data
        representation['client']={'id':client.get('id'),'nom':client.get('nom'),'prenom':client.get('prenom')}
        representation['vendeur']=VendeurSerializer(instance.vendeur,many=False).data 
        vendeur=VendeurSerializer(instance.vendeur,many=False).data
        return representation 
    class Meta:
        model = Vente
        fields = "__all__"
        
class FactureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Facture
        fields = "__all__"