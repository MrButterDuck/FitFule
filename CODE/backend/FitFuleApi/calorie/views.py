from rest_framework import viewsets
from .models import Product
from .serializers import ProductSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .filters import ProductFilter
from django_filters.rest_framework import DjangoFilterBackend


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter
