from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Depot(models.Model):
    id = models.AutoField(primary_key=True)
    nom  = models.CharField(max_length=50)
    adresse = models.CharField(max_length=50)
    telephone = models.CharField(max_length=20)
    nif = models.CharField(max_length=30)
    
    def __str__(self):
        return f"{self.nom} à {self.adresse}"
    
class Vendeur(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,related_name='user_perso', on_delete=models.PROTECT,null=True,blank=True)
    adresse = models.CharField(max_length = 50)
    cni = models.CharField(max_length=50)
    telephone = models.CharField(max_length=20)
    code = models.CharField(editable=False,max_length=100,null=True,unique=True)
    
    def __str__(self):
        return f"{self.id}"

class Produit(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User,related_name='user_prod', on_delete=models.PROTECT,null=True,blank=True,editable=False)
    nom_produit = models.CharField(max_length=100)
    quantite = models.FloatField()
    prix_unitaire = models.FloatField()
    prix_total = models.FloatField(editable=False)
    date = models.DateField(auto_now=True,editable=False)
    
    def __str__(self):
        return f"{self.nom_produit}"

class Client(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    adresse = models.CharField(max_length=50)
    telephone = models.CharField(max_length=20)
    
    def __str__(self):
        return f"{self.nom} {self.prenom}"
class Stock(models.Model):
    id = models.AutoField(primary_key=True)
    produit = models.ForeignKey(Produit,related_name='produit_stock',on_delete=models.PROTECT,null=True,blank=True)
    entrees = models.FloatField(editable=False)
    quantite_restante = models.FloatField(null=True,editable=False)
    date_entree = models.DateField(auto_now=True,editable=False)
    date_sortie = models.DateField(null=True)
    sorties = models.FloatField(editable=False,default=0)
    
    def __str__(self):
        return f"Quantite entrant :{self.entrees} "
    
class Vente(models.Model):
    id = models.AutoField(primary_key=True)
    user=models.ForeignKey(User,related_name='user_vente',on_delete=models.PROTECT,null=True,blank=True,editable=False)
    stock = models.ForeignKey(Stock,related_name='stock_vente',on_delete=models.PROTECT,null=True,blank=True)
    vendeur = models.ForeignKey(Vendeur,related_name='vendeur_vente',on_delete=models.PROTECT,null=True,blank=True)
    client = models.ForeignKey(Client,related_name='client_vente',on_delete=models.PROTECT,null=True,blank=True)
    date_vente = models.DateField(auto_now=True,editable=False)
    quantite = models.IntegerField()
    prix_vente = models.FloatField(editable=False)
    
    def __str__(self):
        return f"{self.quantite} pour {self.prix_vente}"
    
    

        
    
    
