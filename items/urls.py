from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import Items

router = DefaultRouter()
router.register(r'items', Items, basename='item')  # Changed basename to 'item'

urlpatterns = [
    path('', include(router.urls)),
]
