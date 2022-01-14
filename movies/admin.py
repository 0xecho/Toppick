from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.Movie)
admin.site.register(models.Genre)
admin.site.register(models.MovieSeen)
admin.site.register(models.MovieComparision)
admin.site.register(models.Director)