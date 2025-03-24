from django.contrib import admin
from .models import Recipe, RecipeIngredient


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1  # Количество пустых строк для добавления


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'preparation_time',
        'difficulty',
        'calories',
        'proteins',
        'fats',
        'carbohydrates',
        'total_weight',
        'price',
        'meal_type',
        'is_vegan'
    )
    search_fields = ('name',)
    list_filter = ('difficulty',)
    inlines = [RecipeIngredientInline]


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'product', 'quantity')
    search_fields = ('recipe__name', 'product__name')
