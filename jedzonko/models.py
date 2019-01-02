from django.db import models


class Recipe(models.Model):
    name = models.CharField(max_length=255)
    ingredients = models.TextField()
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    preparation_time = models.SmallIntegerField()
    votes = models.IntegerField(default=0)
    preparation = models.TextField()


class Plan(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)


class Recipeplan(models.Model):
    name_of_day = (
        (1,"Poniedziałek"),
        (2,"Wtorek"),
        (3,"Środa"),
        (4,"Czwartek"),
        (5,"Piątek"),
        (6,"Sobota"),
        (7,"Niedziela")
    )

    meal_name = models.CharField(max_length=255)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    order = models.SmallIntegerField()
    day_name = models.SmallIntegerField(choices=name_of_day)


class Page(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    slug = models.SlugField(max_length=255)
