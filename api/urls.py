# pages/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('getRoute', get_route),
    path('insertNode', insert_node),
    path('modifyNode', modify_node),
    path('deleteNode', delete_node),
    path('getKeys', get_api_keys),
    path('getTrafficData', get_traffic_data),
    path('login_user', login_user),
    path('signup_user', signup_user),
    path('logout_user', logout_user)
]
