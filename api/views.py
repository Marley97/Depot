from django.shortcuts import render
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db import transaction
from rest_framework.response import Response
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, mixins
from rest_framework.views import APIView
from rest_framework import viewsets
from .serializers import *
from .models import *

class TokenPairView(TokenObtainPairView):
    serializer_class = TokenPairSerializer
    
class GroupViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = IsAuthenticated,
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all().order_by('-id')
    
class DepotViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = IsAuthenticated,
    queryset = Depot.objects.all()
    serializer_class = DepotSerializer
    
class VendeurViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = IsAuthenticated,
    queryset = Vendeur.objects.all()
    serializer_class = VendeurSerializer
    
    @transaction.atomic
    def create(self, request):
        user = request.user
        data = request.data
        vendeur = Vendeur(
            user = user,
            adresse = data.get('adresse'),
            telephone = data.get('telephone'),
            cni = data.get('cni')
        )
        vendeur.save()
        serializer = VendeurSerializer(vendeur,many=False).data
        return Response(serializer,201)
    
class ProduitViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = IsAuthenticated,
    queryset = Produit.objects.all()
    serializer_class = ProduitSerializer
    @transaction.atomic
    def create(self,request):
        data = request.data
        user = request.user
        nom_produit = data.get('nom_produit')
        date_fabrication = data.get('date_fabrication')
        date_expiration = data.get('date_expiration')
        quantite = float(data.get('quantite'))
        prix_unitaire = float(data.get('prix_unitaire'))
        prix_total = float(quantite)*float(prix_unitaire)
        
        produit:Produit = Produit(
            user = request.user,
            nom_produit = nom_produit,
            date_fabrication = date_fabrication,
            date_expiration = date_expiration,
            quantite = quantite,
            prix_unitaire = prix_unitaire,
            prix_total = prix_total    
        )
        produit.save()
        stock:Stock = Stock.objects.filter(produit__nom_produit=produit.nom_produit,produit__date_fabrication=produit.date_fabrication,produit__date_expiration=date_expiration)
        if stock:
            stock[0].entrees+=float(quantite)
            stock[0].save()
        else:
            stock1:Stock=Stock(
                produit = produit,
                entrees = produit.quantite,
                sorties = produit.quantite
            )
            stock1.save()    
        return Response({'Status': 'Produit ajouter avec succès'}, 201)                 
class ClientViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = IsAuthenticated,
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    
class StockViewSet(viewsets.ModelViewSet):     
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = IsAuthenticated,
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    
class EmplacementViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = IsAuthenticated,
    queryset = Emplacement.objects.all()
    serializer_class = EmplacementSerializer
    @transaction.atomic
    def create(self,request):
        data = request.data
        user = request.user
        numero_etagere = data.get('numero_etagere')
        numero_colonne = data.get('numero_colonne')
        stock:Stock = Stock.objects.get(id=int(data.get('stock')))
        emplacement:Emplacement=Emplacement(
            numero_colonne = numero_colonne,
            numero_etagere = numero_etagere,
            stock = stock
        )
        emplacement.save()
        return Response({'Status': 'Emplacement ajouter avec succès'}, 201)  
    
class VenteViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = IsAuthenticated,
    queryset = Vente.objects.all()
    serializer_class = VenteSerializer
    @transaction.atomic
    def create(self,request):
        data = request.data
        user = request.user
        quantite = float(data.get('quantite'))
        stock:Stock = Stock.objects.get(id=data.get('stock'))
        vendeur:Vendeur = Vendeur.objects.get(id=int(data.get('vendeur')))
        client:Client = Client.objects.get(id=int(data.get('client')))
        prix_vente = quantite*stock.produit.prix_unitaire
        vente:Vente=Vente(
            user =request.user,
            quantite =quantite,
            prix_vente = prix_vente,
            stock = stock,
            vendeur = vendeur,
            client =client
        )
        vente.save()
        stock.sorties -=vente.quantite
        stock.save()
        return Response({'Status': 'Vente effectuer avec succès'}, 201)
        
    
class FactureViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = IsAuthenticated,
    queryset = Facture.objects.all()
    serializer_class = FactureSerializer
    @transaction.atomic
    def create(self,request):
        data = request.data
        user = request.user
        numero_facture = data.get(numero_facture)
        vente:Vente = Vente.objects.get(id=int(data.get('vente')))
        depot:Depot = Depot.objects.get(id=int(data.get('depot')))
        facture:Facture=Facture(
            user = request.user,
            numero_facture =numero_facture,
            vente = vente,
            depot = depot
        )
        facture.save()
        return Response({'Status': 'Facture  generer avec succès'}, 201) 
        
        
        
        