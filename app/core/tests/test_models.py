from django.test import TestCase
from core import models


def sample_recipe(**params):
    defaults = {
        'name': 'Butter Pie',
    }
    defaults.update(params)

    return models.Recipe.objects.create(**defaults)


class TestModels(TestCase):

    def test_ingredient_str(self):
        """
        Test the ingredient string representation
        """
        recipe = sample_recipe()

        ingredient = models.Ingredient.objects.create(
            name='Goji berries',
            recipe=recipe
        )

        self.assertEqual(str(ingredient), ingredient.name)

    def test_recipe_str(self):
        """
        Test the recipe string representation
        """
        recipe = models.Recipe.objects.create(
            name='Shark infested custard',
        )

        self.assertEqual(str(recipe), recipe.name)
