# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets

from core.models import Recipe
from recipe.serializers import RecipeSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    """Manage recipes in the database"""
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()
