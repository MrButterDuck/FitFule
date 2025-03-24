from django.contrib.auth.models import AbstractUser
from django.db import models
from menu.models import Recipe
from calorie.models import Product

  
class CustomUser(AbstractUser):
    age = models.PositiveIntegerField(null=True, blank=True)
    height = models.PositiveIntegerField(null=True, blank=True)
    weight = models.PositiveIntegerField(null=True, blank=True)
    favorites = models.ManyToManyField(
        Product, blank=True, related_name='favorited_by'
    )
    allergy = models.ManyToManyField(
        Product, blank=True, related_name='allergies'
    )
    goal = models.CharField(
        max_length=50, choices=[
            ('mass_gain', 'Набор массы'),
            ('weight_loss', 'Сброс веса'),
            ('weight_maintenance', 'Поддержание веса'),
        ], null=True, blank=True
    )  # Цель
    activity_level = models.CharField(
        max_length=50, choices=[
            ('low', 'Низкий'),
            ('moderate', 'Умеренный'),
            ('high', 'Высокий'),
        ], null=True, blank=True
    )  # Уровень физической активности

    def __str__(self):
        return self.username


class CalorieCalculationHistory(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    calorie_need = models.PositiveIntegerField()
    goal = models.CharField(
        max_length=50, choices=[
            ('mass_gain', 'Набор массы'),
            ('weight_loss', 'Сброс веса'),
            ('weight_maintenance', 'Поддержание веса'),
        ]
    )  # Цель на данный расчет
    activity_level = models.CharField(
        max_length=50, choices=[
            ('low', 'Низкий'),
            ('moderate', 'Умеренный'),
            ('high', 'Высокий'),
        ]
    )  # Уровень физической активности


class SavedMenu(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='saved_menus')
    recipes = models.ManyToManyField(Recipe)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Menu for {self.user.username} at {self.created_at:%Y-%m-%d %H:%M}"