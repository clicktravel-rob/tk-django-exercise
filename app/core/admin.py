# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from core import models

admin.site.register(models.Ingredient)
admin.site.register(models.Recipe)
