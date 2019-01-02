"""scrumlab URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from jedzonko.views import *



urlpatterns = [
    path('add', add_test_data_to_database),
    path('admin/', admin.site.urls),
    re_path(r'^$', LandingPage.as_view()),
    re_path(r'^main$', MainPage.as_view()),
    re_path(r'^recipe/(?P<id>\d+)$', RecipeDetails.as_view()),
    re_path(r'^recipe/list/$', Recipe_List.as_view()),
    re_path(r'^recipe/add$', RecipeAdd.as_view()),
    # re_path(r'^recipe/modify/(?P<id>\d+)$', ),
    re_path(r'^plan/(?P<id>\d+)$', PlanDetails.as_view()),
    re_path(r'^plan$', PlanList.as_view()),
    re_path(r'^plan/add$', PlanAdd.as_view()),
    re_path(r'^plan/add/details$', PlanAddDetails.as_view()),
    re_path('^contact', ContactView.as_view()),
    re_path('^about', AboutView.as_view()),
    re_path('^new_plan_details', PlanReady.as_view()),
]

