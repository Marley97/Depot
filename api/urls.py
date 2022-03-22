from django.urls import path, include
from rest_framework import routers
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView,TokenObtainPairView
router = routers.DefaultRouter()

router.register("groups", GroupViewSet)
router.register("depot",DepotViewSet)
router.register("vendeur",VendeurViewSet)
router.register("produit",ProduitViewSet)
router.register("client",ClientViewSet)
router.register("stock",StockViewSet)
router.register("vente",VenteViewSet)
urlpatterns = [
    path('', include(router.urls)),
    path('login/', TokenPairView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
    path('api_auth', include('rest_framework.urls')),

]