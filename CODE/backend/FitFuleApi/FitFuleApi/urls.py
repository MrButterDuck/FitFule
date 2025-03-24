from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import routers, permissions
from calorie.views import ProductViewSet
from menu.views import RecipeViewSet
from account.views import UserViewSet
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

router = routers.DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'recipes', RecipeViewSet, basename='recipe')
router.register(r'users', UserViewSet, basename='user')

schema_view = get_schema_view(
    openapi.Info(
        title="FitFuel API",
        default_version='v1',
        description="Документация для API веб-сервиса FitFuel",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@fitfuel.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/auth/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.jwt')),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # Redoc UI
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
