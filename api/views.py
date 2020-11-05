from django.http import HttpResponse, HttpResponseBadRequest
import json
from ddb_actions import get_route_record

#Set this in config, should be set using auth header later
USER = 'user'

def index(request):
    return HttpResponse()

def getRoute(request):
    """ Expect the json fields route. """
    json_data = json.loads(request.body)
    try:
        route = json_data["route"]
        get_route_record(USER, route)
    except KeyError:
        HttpResponseBadRequest("Malformed Input")
    return HttpResponse()

def insertNode(request):
    return HttpResponse()

def modifyNode(request):
    return HttpResponse()

def deleteNode(request):
    return HttpResponse()

