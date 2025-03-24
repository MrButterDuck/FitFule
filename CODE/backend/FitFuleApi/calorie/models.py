from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    calories = models.FloatField()        # калорийность (на 100 г или порцию)
    proteins = models.FloatField()
    fats = models.FloatField()
    carbohydrates = models.FloatField()

    def __str__(self):
        return self.name
