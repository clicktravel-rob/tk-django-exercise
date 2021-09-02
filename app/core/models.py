# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Recipe(models.Model):
    """
    A recipe containing various ingredients
    """
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=512)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """
    Ingredient to be used in a recipe
    """
    name = models.CharField(max_length=255)
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredients',
    )

    def __str__(self):
        return self.name
