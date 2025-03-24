from django.db import models
from calorie.models import Product


class Recipe(models.Model):
    MEAL_TYPE_CHOICES = [
        ('breakfast', 'Завтрак'),
        ('lunch', 'Обед'),
        ('dinner', 'Ужин'),
        ('snack', 'Перекус'),
    ]
    name = models.CharField(max_length=255)
    preparation_time = models.PositiveIntegerField(
        help_text="Время приготовления в минутах"
    )
    difficulty = models.CharField(max_length=50)
    calories = models.FloatField(default=0)
    proteins = models.FloatField(default=0)
    fats = models.FloatField(default=0)
    carbohydrates = models.FloatField(default=0)
    total_weight = models.FloatField(default=0)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    meal_type = models.CharField(
        max_length=20,
        choices=MEAL_TYPE_CHOICES,
        default='lunch')
    is_vegan = models.BooleanField(default=False)
    ingredients = models.ManyToManyField(
        Product,
        through='RecipeIngredient',
        related_name='recipes'
    )

    def compute_nutrition(self):
        total_weight = 0
        total_calories = 0
        total_proteins = 0
        total_fats = 0
        total_carbs = 0
        for ri in self.recipe_ingredients.all():
            total_weight += ri.quantity
            total_calories += ri.product.calories * ri.quantity / 100
            total_proteins += ri.product.proteins * ri.quantity / 100
            total_fats += ri.product.fats * ri.quantity / 100
            total_carbs += ri.product.carbohydrates * ri.quantity / 100
        if total_weight > 0:
            self.calories = total_calories * 100 / total_weight
            self.proteins = total_proteins * 100 / total_weight
            self.fats = total_fats * 100 / total_weight
            self.carbohydrates = total_carbs * 100 / total_weight
            self.total_weight = total_weight
        else:
            self.calories = self.proteins = self.fats = self.carbohydrates = self.total_weight = 0

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.compute_nutrition()
        super().save(update_fields=[
            'calories',
            'proteins',
            'fats',
            'carbohydrates',
            'total_weight'
        ])

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        related_name='recipe_ingredients',
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.FloatField(help_text="Количество в граммах")

    def __str__(self):
        return f"{self.product.name} - {self.quantity}g"
