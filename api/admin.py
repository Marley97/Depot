from django.contrib import admin
from . models import *

# Register your models here.
admin.site.register(Depot)
admin.site.register(Vendeur)
admin.site.register(Produit)
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
	list_display = "nom","prenom","adresse","telephone"
	list_filter = "nom",
	search_fields = "nom","prenom"
admin.site.register(Stock)
admin.site.register(Emplacement)
admin.site.register(Vente)
admin.site.register(Facture)
