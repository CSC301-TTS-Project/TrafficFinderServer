# pages/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('getRoute', get_route),
    path('insertNode', insert_node),
    path('modifyNode', modify_node),
    path('deleteNode', delete_node),
    path('getTrafficData', get_traffic_data)
]
