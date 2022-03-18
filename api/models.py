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
        return f"Nom :{self.nom} Adresse :{self.adresse}"
    
class Vendeur(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,related_name='user_perso', on_delete=models.PROTECT,null=True,blank=True)
    adresse = models.CharField(max_length = 50)
    cni = models.CharField(max_length=50)
    telephone = models.CharField(max_length=20)
    
    def __str__(self):
        return f"Nom:{self.user.first_name}"

class Produit(models.Model):
    id = models.BigAutoField(primary_key=True)
    nom_produit = models.CharField(max_length=100)
    quantite = models.FloatField()
    prix_unitaire = models.FloatField()
    prix_total = models.FloatField(editable=False)
    date_fabrication = models.DateField()
    date_expiration = models.DateField()
    date = models.DateField(auto_now=True,editable=False)
    
    def __str__(self):
        return f"Nom:{self.nom_produit}"

class Client(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    adresse = models.CharField(max_length=50)
    telephone = models.CharField(max_length=20)
    
    def __str__(self):
        return f"Nom :{self.nom} Prenom:{self.prenom}"
class Stock(models.Model):
    id = models.AutoField(primary_key=True)
    produit = models.ForeignKey(Produit,related_name='produit_stock',on_delete=models.PROTECT,null=True,blank=True)
    entrees = models.FloatField(editable=False)
    sorties = models.FloatField(editable=False)
    date_entree = models.DateField(auto_now=True,editable=False)
    date_sortie = models.DateField(null=True)
    
    def __str__(self):
        return f"Entress :{self.entrees} Sorties :{self.sorties}"
    
class Emplacement(models.Model):
    id = models.AutoField(primary_key=True)
    numero_etagere = models.CharField(max_length=20)
    numero_colonne = models.CharField(max_length=20)
    stock = models.ForeignKey(Stock,related_name="stock_emplacement",on_delete=models.PROTECT,null=True,blank=True)
    def __str__(self):
        return f"NUmero:{self.numero_etagere}"
    
class Vente(models.Model):
    id = models.AutoField(primary_key=True)
    user=models.ForeignKey(User,related_name='user_vente',on_delete=models.PROTECT,null=True,blank=True,editable=False)
    stock = models.ForeignKey(Stock,related_name='stock_vente',on_delete=models.PROTECT,null=True,blank=True)
    vendeur = models.ForeignKey(Vendeur,related_name='vendeur_vente',on_delete=models.PROTECT,null=True,blank=True)
    client = models.ForeignKey(Client,related_name='client_vente',on_delete=models.PROTECT,null=True,blank=True)
    date_vente = models.DateField(auto_now=True,editable=False)
    quantite = models.IntegerField()
    prix_vente = models.FloatField(editable=False)
    
class Facture(models.Model):
    id = models.AutoField(primary_key=True)
    vente = models.ForeignKey(Vente,on_delete=models.PROTECT,null=True,blank=True)
    numero_facture = models.CharField(max_length=20)
    depot = models.ForeignKey(Depot,related_name='depot',on_delete=models.PROTECT,null=True,blank=True)
    date_facture = models.DateField(auto_now=True,editable=False)
    prix_total = models.IntegerField()
    
    def __str__(self):
        return f"NUmero:{self.numero_facture}"
    
    

        
    
    
