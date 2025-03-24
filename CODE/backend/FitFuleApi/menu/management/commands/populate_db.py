import random
from django.core.management.base import BaseCommand
from menu.models import Recipe, RecipeIngredient
from calorie.models import Product


class Command(BaseCommand):
    help = "Populate the database with sample Products and Recipes."

    def handle(self, *args, **options):
        self.stdout.write("Начинаем заполнение базы данных...")

        # Список реальных названий продуктов (50 наименований)
        product_names = [
            "Куриное филе", "Говядина", "Свинина", "Лосось", "Тунец",
            "Креветки", "Мидии", "Брокколи", "Цветная капуста", "Морковь",
            "Свекла", "Помидоры", "Огурцы", "Салат айсберг", "Шпинат",
            "Капуста", "Картофель", "Рис", "Паста", "Киноа",
            "Овсяные хлопья", "Хлеб цельнозерновой", "Яблоки", "Бананы", "Апельсины",
            "Груши", "Киви", "Виноград", "Клубника", "Малина",
            "Черника", "Авокадо", "Яйца", "Молоко", "Творог",
            "Сыр пармезан", "Греческий йогурт", "Миндаль", "Орехи грецкие", "Фундук",
            "Семена чиа", "Льняное семя", "Мёд", "Оливковое масло", "Кокосовое масло",
            "Соевый соус", "Бальзамический уксус", "Лимон", "Чеснок", "Имбирь"
        ]

        # Создаем 50 продуктов с реальными именами
        for name in product_names:
            # Генерируем случайные значения (данные указаны на 100 грамм)
            calories = round(random.uniform(50, 300), 2)
            proteins = round(random.uniform(0, 20), 2)
            fats = round(random.uniform(0, 20), 2)
            carbohydrates = round(random.uniform(10, 50), 2)

            product, created = Product.objects.get_or_create(
                name=name,
                defaults={
                    'calories': calories,
                    'proteins': proteins,
                    'fats': fats,
                    'carbohydrates': carbohydrates,
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Создан продукт: {name}"))
            else:
                self.stdout.write(f"Продукт уже существует: {name}")

        # Получаем список всех продуктов для использования в рецептах
        products = list(Product.objects.all())

        # Список реальных названий рецептов (20 наименований)
        recipe_names = [
            "Куриный салат с авокадо",
            "Говяжий стейк с овощами",
            "Суп минестроне",
            "Лосось с брокколи на пару",
            "Паста Болоньезе",
            "Салат Цезарь",
            "Ризотто с грибами",
            "Плов с курицей",
            "Омлет с шампиньонами",
            "Греческий салат",
            "Тунец с киноа",
            "Борщ с говядиной",
            "Креветки в чесночном соусе",
            "Паста с соусом песто",
            "Запечённая свинина с картофелем",
            "Рыба с лимоном",
            "Салат из свежих овощей",
            "Сэндвич с тунцом",
            "Куриное филе в апельсиновом соусе",
            "Вегетарианский кускус с овощами"
        ]

        difficulties = ["Легкий", "Средний", "Сложный"]
        meal_types = ['breakfast', 'lunch', 'dinner', 'snack']

        # Создаем 20 рецептов с реальными названиями
        for i, recipe_name in enumerate(recipe_names, start=1):
            preparation_time = random.randint(10, 90)  # время приготовления в минутах
            difficulty = random.choice(difficulties)
            meal_type = random.choice(meal_types)
            price = round(random.uniform(100, 500), 2)
            is_vegan = random.choice([True, False])
            
            recipe = Recipe.objects.create(
                name=recipe_name,
                preparation_time=preparation_time,
                difficulty=difficulty,
                calories=0,     # позже пересчитаем по ингредиентам
                proteins=0,
                fats=0,
                carbohydrates=0,
                total_weight=0,
                price=price,
                meal_type=meal_type,
                is_vegan=is_vegan
            )
            
            # Выбираем от 3 до 7 случайных продуктов для рецепта
            num_ingredients = random.randint(3, 7)
            chosen_products = random.sample(products, num_ingredients)

            for product in chosen_products:
                quantity = random.randint(50, 300)  # количество в граммах
                RecipeIngredient.objects.create(
                    recipe=recipe,
                    product=product,
                    quantity=quantity
                )
            
            # Пересчет нутриентов рецепта
            total_calories = 0
            total_proteins = 0
            total_fats = 0
            total_carbs = 0
            total_weight = 0

            for ri in recipe.recipe_ingredients.all():
                factor = ri.quantity / 100.0
                total_calories += ri.product.calories * factor
                total_proteins += ri.product.proteins * factor
                total_fats += ri.product.fats * factor
                total_carbs += ri.product.carbohydrates * factor
                total_weight += ri.quantity

            recipe.calories = round(total_calories, 2)
            recipe.proteins = round(total_proteins, 2)
            recipe.fats = round(total_fats, 2)
            recipe.carbohydrates = round(total_carbs, 2)
            recipe.total_weight = total_weight
            recipe.save()

            self.stdout.write(self.style.SUCCESS(f"Создан рецепт: {recipe_name}"))

        self.stdout.write(self.style.SUCCESS("Заполнение базы данных завершено успешно."))
