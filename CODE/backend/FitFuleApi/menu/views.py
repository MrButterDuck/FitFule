# import io
# from django.http import HttpResponse
# from django.db.models import Q
# from rest_framework.decorators import action
# from reportlab.pdfgen import canvas
# from rest_framework.response import Response
from rest_framework import viewsets
from .models import Recipe
from .serializers import RecipeSerializer, RecipeCreateUpdateSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from .filters import RecipeFilter
from .pagination import RecipePagination


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter
    pagination_class = RecipePagination

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return RecipeCreateUpdateSerializer
        return RecipeSerializer

    # @action(detail=False, methods=['get'], url_path='filter-menu')
    # def filter_menu(self, request):
    #     budget = request.query_params.get('budget')
    #     calorie_count = request.query_params.get('calorieCount')
    #     calorie_unit = request.query_params.get('calorieUnit')
    #     meal_times = request.query_params.getlist('mealTimes')
    #     ingredient_ids = request.query_params.getlist('ingredients')
    #     is_vegan = request.query_params.get('isVegan')
    #     consider_allergies = request.query_params.get('considerAllergies')

    #     filters = Q()

    #     # Фильтрация по бюджету (максимальная цена)
    #     if budget:
    #         try:
    #             budget_val = float(budget)
    #             filters &= Q(price__lte=budget_val)
    #         except ValueError:
    #             pass

    #     # Фильтрация по калориям (учёт единиц измерения)
    #     if calorie_count:
    #         try:
    #             calorie_val = float(calorie_count)
    #             if calorie_unit == 'kj':
    #                 calorie_val = calorie_val / 4.184
    #             lower_bound = calorie_val * 0.8
    #             upper_bound = calorie_val * 1.2
    #             filters &= Q(calories__gte=lower_bound, calories__lte=upper_bound)
    #         except ValueError:
    #             pass

    #     # По времени приёма пищи
    #     if meal_times:
    #         filters &= Q(meal_type__in=meal_times)

    #     # Фильтрация по ингредиентам (хотя бы один из выбранных)
    #     if ingredient_ids:
    #         filters &= Q(ingredients__id__in=ingredient_ids)

    #     # Веганский фильтр
    #     if is_vegan in ['true', 'True', '1']:
    #         filters &= Q(is_vegan=True)

    #     # Исключаем рецепты, содержащие аллергены пользователя (если выбран флаг и пользователь авторизован)
    #     if consider_allergies in ['true', 'True', '1'] and request.user.is_authenticated:
    #         user_allergy_ids = request.user.allergy.values_list('id', flat=True)
    #         filters &= ~Q(ingredients__id__in=user_allergy_ids)

    #     qs = self.queryset.filter(filters).distinct()
    #     serializer = RecipeSerializer(qs, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    # @action(detail=False, methods=['post'], url_path='export-pdf')
    # def export_pdf(self, request):
    #     """
    #     Принимает в теле запроса параметр "menu" (список рецептов или их id) и возвращает PDF.
    #     """
    #     menu_data = request.data.get('menu')
    #     if not menu_data:
    #         return Response({"detail": "Меню не предоставлено"}, status=status.HTTP_400_BAD_REQUEST)

    #     recipe_ids = []
    #     for item in menu_data:
    #         if isinstance(item, dict) and 'id' in item:
    #             recipe_ids.append(item['id'])
    #         else:
    #             recipe_ids.append(item)

    #     recipes = self.queryset.filter(id__in=recipe_ids)

    #     # Генерируем PDF с помощью ReportLab
    #     buffer = io.BytesIO()
    #     pdf = canvas.Canvas(buffer)
    #     y = 800
    #     pdf.setFont("Helvetica-Bold", 16)
    #     pdf.drawString(100, y, "Ваше меню")
    #     y -= 40
    #     pdf.setFont("Helvetica", 12)
    #     for recipe in recipes:
    #         pdf.drawString(50, y, f"Рецепт: {recipe.name}")
    #         pdf.drawString(300, y, f"Калорийность: {recipe.calories} kcal, Цена: {recipe.price}")
    #         y -= 20
    #         if y < 50:
    #             pdf.showPage()
    #             y = 800
    #     pdf.showPage()
    #     pdf.save()
    #     buffer.seek(0)
    #     response = HttpResponse(buffer, content_type='application/pdf')
    #     response['Content-Disposition'] = 'attachment; filename="menu.pdf"'
    #     return response
