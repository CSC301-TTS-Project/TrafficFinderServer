# pages/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('', hdc_index),
    path('getRoute', hdc_getRoute),
    path('insertNode', hdc_insertNode),
    path('modifyNode', hdc_modifyNode),
    path('deleteNode', hdc_deleteNode),
    path('addNodeToRoute', hdc_addNodeToRoute),
    path('modifyRouteNode', hdc_modifyRouteNode),
    path('deleteRouteNode', hdc_deleteRouteNode),
    path('getTrafficData', hdc_getTrafficData)
]
