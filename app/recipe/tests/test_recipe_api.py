from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe, Ingredient


RECIPES_URL = reverse('recipe:recipe-list')


def sample_recipe(**params):
    """Create and return a sample recipe"""
    defaults = {
        'name': 'Sample recipe',
        'description': 'Lovely food',
    }
    defaults.update(params)

    return Recipe.objects.create(**defaults)


def detail_url(recipe_id):
    """Return recipe detail url"""
    return reverse('recipe:recipe-detail', args=[recipe_id])


class RecipeApiTestCase(TestCase):
    """
    Test recipe API
    """

    def setUp(self):
        self.client = APIClient()

    def test_list_recipes(self):
        """
        Test listing existing RecipeSerializer
        """
        recipe1 = Recipe.objects.create(name='Prawn salad')
        recipe2 = Recipe.objects.create(name='Cheese pie')

        print(RECIPES_URL)

        response = self.client.get(RECIPES_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0].get('name'), recipe1.name)
        self.assertEqual(response.data[1].get('name'), recipe2.name)

    def test_show_recipe_detail(self):
        """
        Test retrieving the details for a single recipes
        """
        recipe = sample_recipe()
        response = self.client.get(detail_url(recipe.id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('name'), recipe.name)

    def test_create_recipe(self):
        """
        Test creating a basic recipe
        """
        ingredient_name_1 = 'Cabbage'
        ingredient_name_2 = 'Water'

        data = {
            'name': 'Cabbage soup',
            'description': 'Soup made from cabbage',
            'ingredients': [
                {'name': ingredient_name_1},
                {'name': ingredient_name_2},
            ]
        }
        response = self.client.post(RECIPES_URL, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        recipes = Recipe.objects.all()

        self.assertEqual(len(recipes), 1)
        self.assertEqual(recipes[0].name, data['name'])
        self.assertEqual(recipes[0].description, data['description'])

        ingredient_names = Ingredient.objects.filter(
            recipe=response.data['id']
        ).values_list("name", flat=True)
        self.assertIn(ingredient_name_1, ingredient_names)
        self.assertIn(ingredient_name_2, ingredient_names)

    def test_delete_recipe(self):
        """Test deleting an existing recipe"""
        recipe = sample_recipe(
            name='Moose burger',
            description='First catch your moose...'
        )
        url = detail_url(recipe.id)

        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Recipe.objects.filter(pk=recipe.id).exists())

    def test_partial_update_recipe_name(self):
        """test updating the name of a recipe only"""
        recipe = sample_recipe(
            name='Cheeseburger',
            description='A burger with cheese on'
        )
        url = detail_url(recipe.id)
        payload = {
            'name': 'Vegan Cheeseburger',
        }

        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.data['name'], payload.get('name'))
        self.assertNotEqual(len(res.data['description']), 0)

    def test_partial_update_recipe_ingredients(self):
        """test updating the ingredients assigned to a recipe"""
        recipe = sample_recipe(
            name='Vegan Cheeseburger',
            description='A burger with vegan cheese on'
        )
        url = detail_url(recipe.id)
        Ingredient.objects.create(
            name='Burger', recipe=recipe
        )
        Ingredient.objects.create(
            name='Cheese', recipe=recipe
        )
        new_ingredient_name_1 = 'Vegiburger'
        new_ingredient_name_2 = 'Vegan cheese'
        payload = {
            'ingredients': [
                {'name': new_ingredient_name_1},
                {'name': new_ingredient_name_2},
            ]
        }

        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.data['name'], recipe.name)
        self.assertEqual(len(res.data.get('ingredients')), 2)

        new_ingredient_names = [
            new_ingredient_name_1,
            new_ingredient_name_2,
        ]

        self.assertIn(
            res.data['ingredients'][0].get('name'),
            new_ingredient_names,
        )
        self.assertIn(
            res.data['ingredients'][1].get('name'),
            new_ingredient_names,
        )
