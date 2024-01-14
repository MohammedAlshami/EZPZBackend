# appname/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("get_components_data/", views.get_components_data, name="get_components_data"),
    path("get_hero_data/", views.get_hero_data, name="get_hero_data"),
    path("get_navbar_data/", views.get_navbar_data, name="get_navbar_data"),
    path("get_footer_data/", views.get_footer_data, name="get_footer_data"),
    path("get_features_data/", views.get_features_data, name="get_features_data"),
    path("get_website_url/", views.get_website_url, name="get_website_url"),
    path(
        "get_website_by_uuid/<str:website_uuid>/",
        views.get_website_by_uuid,
        name="get_website_by_uuid",
    ),
]
