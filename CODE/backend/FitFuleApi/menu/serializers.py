from rest_framework import serializers
from .models import Recipe, RecipeIngredient
from calorie.serializers import ProductSerializer
from calorie.models import Product


class RecipeIngredientSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    
    class Meta:
        model = RecipeIngredient
        fields = ('id', 'product', 'quantity')


class RecipeIngredientCreateSerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product'
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'product_id', 'quantity')


class RecipeSerializer(serializers.ModelSerializer):
    recipe_ingredients = RecipeIngredientSerializer(many=True, read_only=True)
    
    class Meta:
        model = Recipe
        fields = (
            'id', 'name', 'preparation_time', 'difficulty',
            'calories', 'proteins', 'fats', 'carbohydrates',
            'total_weight', 'recipe_ingredients', 'price', 'meal_type',
            'is_vegan'
        )


class RecipeCreateUpdateSerializer(serializers.ModelSerializer):
    recipe_ingredients = RecipeIngredientCreateSerializer(many=True)

    class Meta:
        model = Recipe
        fields = (
            'id', 'name', 'preparation_time',
            'difficulty', 'recipe_ingredients'
        )

    def create(self, validated_data):
        ingredients_data = validated_data.pop('recipe_ingredients')
        recipe = Recipe.objects.create(**validated_data)
        for ingredient_data in ingredients_data:
            RecipeIngredient.objects.create(recipe=recipe, **ingredient_data)
        recipe.compute_nutrition()
        recipe.save()
        return recipe

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('recipe_ingredients', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if ingredients_data is not None:
            instance.recipe_ingredients.all().delete()
            for ingredient_data in ingredients_data:
                RecipeIngredient.objects.create(
                    recipe=instance, **ingredient_data
                )
        instance.compute_nutrition()
        instance.save()
        return instance
