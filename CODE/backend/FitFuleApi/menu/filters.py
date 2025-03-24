import django_filters
from .models import Recipe
from calorie.models import Product


class RecipeFilter(django_filters.FilterSet):
    ids = django_filters.CharFilter(method='filter_by_ids')
    price_min = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    calories = django_filters.CharFilter(method='filter_by_calories')
    meal_type = django_filters.ChoiceFilter(field_name='meal_type', choices=Recipe.MEAL_TYPE_CHOICES)
    exclude_allergens = django_filters.BooleanFilter(method='filter_exclude_allergens')
    include_favorites = django_filters.BooleanFilter(method='filter_include_favorites')
    include_products = django_filters.CharFilter(method='filter_include_products') 

    class Meta:
        model = Recipe
        fields = [
            'ids', 'price_min', 'price_max',
            'calories', 'meal_type', 'exclude_allergens',
            'include_favorites', 'include_products'
        ]

    def filter_by_ids(self, queryset, name, value):
        ids = value.split(',')
        return queryset.filter(id__in=ids)

    def filter_by_calories(self, queryset, name, value):
        if '-' in value:
            try:
                min_calories, max_calories = map(int, value.split('-'))
                return queryset.filter(calories__gte=min_calories, calories__lte=max_calories)
            except ValueError:
                print('error')
                return queryset
    
    def filter_exclude_allergens(self, queryset, name, value):
        user = self.request.user
        if user.is_authenticated and value:
            allergens = user.allergy.all()
            print(allergens)
            return queryset.exclude(ingredients__in=allergens)
        return queryset

    def filter_include_favorites(self, queryset, name, value):
        user = self.request.user
        if user.is_authenticated and value:
            favorites = user.favorites.all()
            return queryset.filter(ingredients__in=favorites)
        return queryset

    def filter_include_products(self, queryset, name, value):
        product_ids = value.split(',')
        return queryset.filter(ingredients__id__in=product_ids).distinct()
