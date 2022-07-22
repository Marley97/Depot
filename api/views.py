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
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
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
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = IsAuthenticated,
    # modification mot de passe

    @transaction.atomic()
    def update(self, request, pk):
        user = self.get_object()
        print(user)
        data = request.data
        username = data.get('username')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        nouv_password = data.get('nouv_password')
        anc_password = data.get('anc_password')
        if user.check_password(anc_password):
            print("checked")
            user.username = username
            user.first_name = first_name
            user.last_name = last_name
            user.set_password(nouv_password)
            user.save()
            return Response({"status": "Utilisateur modifié avec success"}, 201)
        return Response({"status": "Ancien mot de passe incorrect"}, 400)
    
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

    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    search_fields = ['adresse',]
    filterset_fields=['adresse','cni']

    @transaction.atomic()
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        adresse = serializer.validated_data['adresse']
        telephone = serializer.validated_data['telephone']
        cni = serializer.validated_data['cni']
        user = User(
            username=serializer.validated_data['user']['username'],
            first_name=serializer.validated_data['user']['first_name'],
            last_name=serializer.validated_data['user']['last_name'],
            email=serializer.validated_data['user']['email']
        )
        cod = user.username[:3].upper()
        vend = Vendeur.objects.all().last()
        vendeurId = 0
        date = datetime.now()
        year = date.strftime("%y")
        umwaka = year[-3:]
        if vend:
            vendeurId = int(vend.id)+1
        else:
            vendeurId=1
        if vendeurId<10:
            cod= str(cod) +'-'+str(umwaka)+'-0'+str(vendeurId)
        else:
            cod= str(cod) +'-'+str(umwaka)+str(-vendeurId)

        user.set_password(serializer.validated_data['user']['password'])
        vendeur = Vendeur(
            user = request.user,
            adresse = adresse,
            telephone = telephone,
            cni = cni,
            code = cod
        )
        vendeur.save()
        serializer = VendeurSerializer(vendeur,many=False).data
        return Response(serializer,201)

class ProduitViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = IsAuthenticated,
    queryset = Produit.objects.all()
    serializer_class = ProduitSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields={
            'nom_produit':['exact']
    }
    @transaction.atomic
    def create(self,request):
        data = request.data
        user = request.user
        nom_produit = data.get('nom_produit')
        quantite = float(data.get('quantite'))
        prix_unitaire = float(data.get('prix_unitaire'))
        prix_total = float(quantite)*float(prix_unitaire)
        
        produit:Produit = Produit(
            user = request.user,
            nom_produit = nom_produit,
            quantite = quantite,
            prix_unitaire = prix_unitaire,
            prix_total = prix_total    
        )
        produit.save()
        stock:Stock = Stock.objects.filter(produit__nom_produit=produit.nom_produit)
        if stock:
            stock[0].entrees+=float(quantite)
            stock[0].quantite_restante+=float(quantite)
            stock[0].save()
        else:
            stock1:Stock=Stock(
                produit = produit,
                entrees = produit.quantite,
                quantite_restante=produit.quantite
            )
            stock1.save()    
        return Response({'Status': 'Produit ajouter avec succès'}, 201)                 
class ClientViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = IsAuthenticated,
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    search_fields = ['nom','prenom']
    filterset_fields=['nom','prenom']

    
class StockViewSet(viewsets.ModelViewSet):     
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = IsAuthenticated,
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
       
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
        if quantite>stock.quantite_restante or quantite<=0:
            return Response({'Status':'echec,vous n avez pas assez de quantite en stock pour effectuer cette operation'})
        else:    
            vente:Vente=Vente(
                user =request.user,
                quantite =quantite,
                prix_vente = prix_vente,
                stock = stock,
                vendeur = vendeur,
                client =client
            )
            vente.save()
            stock.sorties+=vente.quantite
            stock.quantite_restante -=vente.quantite
            stock.save()
            return Response({'Status': 'Vente effectuer avec succès'}, 201)
        
    
        
        
        
        