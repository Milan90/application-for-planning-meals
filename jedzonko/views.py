import re

from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, Http404
from .models import *
from random import shuffle
from django.shortcuts import render, redirect
from django.views import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def add_test_data_to_database(request):
    """
    Recipe.objects.create(name="Gulasz", ingredients="mięso, papryka, i kilka innych",
                          description="shdbdicnsidyfgnciudygfcyugnifyseivfumxsyerifsrxmirybg",
                          preparation_time=30, votes=99)
    Recipe.objects.create(name="Naleśniki", ingredients="mąka, woda, sól, dżem",
                          description="shdbdicnsidyfgnciudygfcyugnifyseivfumxsyerifsrxmirybg",
                          preparation_time=45, votes=99)
    Recipe.objects.create(name="Gołąbki", ingredients="kapusta, ryż, mięso ",
                          description="shdbdicnsidyfgnciudygfcyugnifyseivfumxsyerifsrxmirybg",
                          preparation_time=240, votes=99)
    Recipe.objects.create(name="koktajl", ingredients="wszystko co masz pod reką",
                          description="shdbdicnsidyfgnciudygfcyugnifyseivfumxsyerifsrxmirybg",
                          preparation_time=30, votes=99)
    Recipe.objects.create(name="Kotlet de volaille", ingredients="askhndirygbc elsrghcmdrgd",
                          description="shdbdicnsidyfgnciudygfcyugnifyseivfumxsyerifsrxmirybg",
                          preparation_time=30, votes=99)
    Recipe.objects.create(name="zapiekanka", ingredients="asfag, sdgvdh, rgdrtgdt, dtrcgtfcgbt",
                          description="shdbdicnsidyfgnciudygfcyugnifyseivfumxsyerifsrxmirybg",
                          preparation_time=30, votes=99)

    Plan.objects.create(name="jak u mamy", description="pozywny i smaczny")
    Plan.objects.create(name="jak u babci", description="mięsko zjedz ziemniaczki zostaw")
    Plan.objects.create(name="jak u cioci", description="lepiej niż na imieninach")
    Plan.objects.create(name="jak u dziadka", description="dawaj wnuczku na drugą")

    Recipeplan.objects.create(meal_name="śniadanie", order=1, day_name=1, plan_id=1, recipe_id=1)
    Recipeplan.objects.create(meal_name="obiad", order=2, day_name=1, plan_id=1, recipe_id=3)
    Recipeplan.objects.create(meal_name="kolacja", order=3, day_name=1, plan_id=1, recipe_id=4)
    Recipeplan.objects.create(meal_name="śniadanie", order=1, day_name=3, plan_id=2, recipe_id=7)
    Recipeplan.objects.create(meal_name="obiad", order=2, day_name=3, plan_id=2, recipe_id=5)
    Recipeplan.objects.create(meal_name="kolacja", order=3, day_name=3, plan_id=2, recipe_id=2)
    Recipeplan.objects.create(meal_name="śniadanie", order=1, day_name=3, plan_id=2, recipe_id=6)
    Recipeplan.objects.create(meal_name="obiad", order=2, day_name=3, plan_id=3, recipe_id=1)
    Recipeplan.objects.create(meal_name="kolacja", order=3, day_name=3, plan_id=3, recipe_id=2)
"""


class LandingPage(View):

    def get(self, request):
        model_lenght = Recipe.objects.count()
        result = [i for i in range(1, model_lenght)]
        shuffle(result)

        recipe = Recipe.objects.get(pk=result[0])
        recipe2 = Recipe.objects.get(pk=result[1])
        recipe3 = Recipe.objects.get(pk=result[2])

        ctx = {"recipe": recipe,
               "recipe2": recipe2,
               "recipe3": recipe3,
               }

        return render(request, "index.html", ctx)


class Recipe_List(View):

    def get(self, request):
        recipes = Recipe.objects.all().order_by("-votes", "-created")

        paginator = Paginator(recipes, 5)
        page = request.GET.get('page')

        try:
            items = paginator.page(page)
        except PageNotAnInteger:
            items = paginator.page(1)  # jeśli nr strony nie będzie liczbą przekieruje na stronę nr 1
        except EmptyPage:  # jeśli nr strony nie będzie przekieruje nas na ostatnią stronę
            items = paginator.page(paginator.num_pages)  # num_pages - całkowita liczba stron - lista

        index = items.number - 1
        max_index = len(paginator.page_range)
        start_index = index - 5 if index >= 5 else 0
        end_index = index + 5 if index <= max_index - 5 else max_index
        page_range = paginator.page_range[start_index:end_index]

        ctx = {
            'recipes': recipes,
            'page_range': page_range,
            'items': items,
        }
        return render(request, "recipes.html", ctx)


class ContactView(View):

    def get(self, request):
        return render(request, "index.html")


class AboutView(View):

    def get(self, request):
        return render(request, "index.html")


class MainPage(View):

    def get(self, request):
        last_plan = Plan.objects.latest("created")
        recipeplans_list = last_plan.recipeplan_set.all().order_by("day_name", "order")
        day_number = 0
        day_list = []
        for element in recipeplans_list:
            if element.day_name != day_number:
                day_list.append(element)
                day_number = element.day_name

        plans_amount = Plan.objects.count()
        recipes_amount = Recipe.objects.count()
        ctx = {
            'plans': plans_amount,
            'recipes': recipes_amount,
            "last_plan": last_plan,
            "recipeplans_list": recipeplans_list,
            "day_list": day_list,
        }
        return render(request, "dashboard.html", ctx)


class RecipeAdd(View):

    def get(self, request):
        return render(request, "app-add-recipe.html")

    def post(self, request):
        recipe_name = request.POST.get("recipe_name")
        recipe_desc = request.POST.get("recipe_desc")
        time_to_prep = request.POST.get("time_to_prep")
        preparation = request.POST.get("preparation")
        ingredients = request.POST.get("ingredients")
        if recipe_name and recipe_desc and time_to_prep and preparation and ingredients:
            Recipe.objects.create(name=recipe_name, ingredients=ingredients, description=recipe_desc,
                                  preparation_time=time_to_prep, preparation=preparation)
            return redirect("/recipe/list/")
        else:
            context = {"message": "Wypełnij poprawnie wszystkie pola",
                       "recipe_name": recipe_name,
                       "recipe_desc": recipe_desc,
                       "time_to_prep": time_to_prep,
                       "preparation": preparation,
                       "ingredients": ingredients,
                       }
            return render(request, "app-add-recipe.html", context)


class RecipeDetails(View):
    def get(self, request, id):
        recipe = Recipe.objects.get(pk=id)
        ingrd = re.split("; |,|:", recipe.ingredients)
        ctx = {
            'recipe': recipe,
            'ingr': ingrd,
        }

        return render(request, "recipe-details.html", ctx)


class PlanList(View):
    def get(self, request):
        plans = Plan.objects.all().order_by("name")

        paginator = Paginator(plans, 3)
        page = request.GET.get('page')

        try:
            items = paginator.page(page)
        except PageNotAnInteger:
            items = paginator.page(1)
        except EmptyPage:
            items = paginator.page(paginator.num_pages)

        index = items.number - 1
        max_index = len(paginator.page_range)
        start_index = index - 5 if index >= 5 else 0
        end_index = index + 5 if index <= max_index - 5 else max_index
        page_range = paginator.page_range[start_index:end_index]

        ctx = {
            'page_range': page_range,
            'items': items,
            'plans': plans,
        }
        return render(request, "app-schedules.html", ctx)


class PlanDetails(View):
    def get(self, request, id):
        plan = Plan.objects.get(pk=id)
        plan_details = plan.recipeplan_set.all().order_by("day_name", "order")
        day_number = 0
        day_list = []
        for element in plan_details:
            if element.day_name != day_number:
                day_list.append(element)
                day_number = element.day_name
        ctx = {
            'plan': plan,
            'plan_details': plan_details,
            'day_list': day_list,
        }
        return render(request, "app-details-schedules.html", ctx)


class PlanAdd(View):
    def get(self, request):
        return render(request, "app-add-schedules.html")

    def post(self, request):
        name = request.POST.get("name")
        description = request.POST.get("description")
        if name and description:
            new_plan = Plan.objects.create(name=name, description=description)
            request.session['plan_id'] = new_plan.id
            return redirect("/plan/add/details")
        else:
            return render(request, "app-add-schedules.html", {'message': "Wypełnij poprawnie wszystkie pola"})


class PlanAddDetails(View):
    def get(self, request):
        if request.session.get("plan_id") is not None:
            plan_id = request.session.get("plan_id")
            ctx = {
                'plan_id': plan_id,
                'recipes': Recipe.objects.all(),
                'plan': Plan.objects.get(id=plan_id),
            }
            return render(request, "app-schedules-meal-recipe.html", ctx)
        else:
            raise PermissionDenied

    def post(self, request):  # get działa posta zrobie jutro
        if int(request.POST.get('plan_id')) == request.session.get("plan_id"):
            new_plan = Plan.objects.get(pk=request.POST.get('plan_id'))
            meal_name = request.POST.get("name")
            recipe = Recipe.objects.get(pk=request.POST.get("recipe"))
            order = request.POST.get("order")
            day_name = request.POST.get("day")
            Recipeplan.objects.create(meal_name=meal_name, recipe=recipe, plan=new_plan, order=order, day_name=day_name)
            return redirect("/plan/add/details")
        else:
            raise Http404


class PlanReady(View):
    def get(self, request):
        del request.session["plan_id"]
        return redirect("/plan")
