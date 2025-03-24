from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import CustomUser
from menu.models import Recipe
from .serializers import CustomUserSerializer
from rest_framework.permissions import IsAuthenticated


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'], url_path='save-menu')
    def save_menu(self, request):
        """
        Экран: /api/users/save-menu/
        Ожидается, что в теле запроса передаётся параметр "menu" (список рецептов или их id).
        Создаётся новый объект SavedMenu для текущего пользователя.
        """
        menu_data = request.data.get('menu')
        if not menu_data:
            return Response({"detail": "Меню не предоставлено"}, status=status.HTTP_400_BAD_REQUEST)

        recipe_ids = []
        for item in menu_data:
            if isinstance(item, dict) and 'id' in item:
                recipe_ids.append(item['id'])
            else:
                recipe_ids.append(item)

        saved_menu = SavedMenu.objects.create(user=request.user)
        recipes = Recipe.objects.filter(id__in=recipe_ids)
        saved_menu.recipes.set(recipes)
        saved_menu.save()
        return Response({"detail": "Меню успешно сохранено"}, status=status.HTTP_201_CREATED)