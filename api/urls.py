# pages/urls.py
from django.urls import path
from .views import *
from rest_framework.authtoken import views

urlpatterns = [
    path('getRoute', get_route),
    path('insertNode', insert_node),
    path('modifyNode', modify_node),
    path('deleteNode', delete_node),
    path('getKeys', get_api_keys),
    path('getTrafficData', get_traffic_data),
    path('getGeoJson', get_route_as_geojson),
    path('login_user', views.obtain_auth_token),
    path('signup_user', signup_user),
]
