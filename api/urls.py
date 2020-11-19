# pages/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('', hdc_index),
    path('getRoute', get_route),
    path('insertNode', insert_node),
    path('modifyNode', hdc_modifyNode),
    path('deleteNode', delete_node),
    path('addNodeToRoute', hdc_addNodeToRoute),
    path('modifyRouteNode', hdc_modifyRouteNode),
    path('deleteRouteNode', hdc_deleteRouteNode),
    path('getTrafficData', get_traffic_data)
]
