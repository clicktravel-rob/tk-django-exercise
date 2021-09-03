from rest_framework import serializers

from core.models import Ingredient, Recipe


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for ingredient objects"""

    class Meta:
        model = Ingredient
        fields = ('id', 'name')
        read_only_fields = ('id',)


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipe objects"""
    ingredients = IngredientSerializer(
        many=True,
    )

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'description', 'ingredients')
        read_only_fields = ('id',)

    def create(self, validated_data):
        ingredient_validated_data = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        for ingredient in ingredient_validated_data:
            ingredient['recipe'] = recipe
            Ingredient.objects.create(**ingredient)
        return recipe

    def update(self, instance, validated_data):
        ingredient_data = validated_data.pop('ingredients', None)
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get(
            'description', instance.description
            )
        instance.save()
        if ingredient_data:
            Ingredient.objects.filter(recipe=instance).delete()
            for ingredient in ingredient_data:
                ingredient['recipe'] = instance
                Ingredient.objects.create(**ingredient)
        return instance
