from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError, JsonResponse
import json
from .ddb_actions import get_route_record, update_route_record, get_segment
from .pg_routing_queries import shortest_route, nearest_node

#Set this in config, should be set using auth header later
USER = 'user'

def index(request):
    return HttpResponse()

def getRoute(request):
    """ Expect the json fields route. """
    json_data = json.loads(request.body)
    try:
        route = json_data["route"]
        route_record = get_route_record(USER, route)
        return JsonResponse(route_record)
    except KeyError:
        return HttpResponseBadRequest("Malformed Input")

def insertNode(request):
    json_data = json.loads(request.body)
    try:
        route = json_data["route"]
        lat = json_data["lat"]
        lng = json_data["lng"]
        segment_idx = json_data["index"]
        new_node = nearest_node(lat, lng)
        if segment_idx == 0:
            update_route_record(USER, route, segment_idx, new_node)
            return JsonResponse(json.dumps(nearest_node))
        else:
            prev_node_segment = get_segment(USER, route, segment_idx - 1)
            prev_nodes_len = prev_node_segment[f"segment_{segment_idx - 1}_length"]
            prev_node = prev_node_segment[f"segment_{segment_idx - 1}"][prev_nodes_len - 1]
            new_segement = shortest_route(prev_node, new_node)
            update_route_record(USER, route, segment_idx, new_segement)
            return JsonResponse(json.dumps(new_segement))
    except KeyError:
        return HttpResponseBadRequest("Malformed Input")

def modifyNode(request):
    return HttpResponse()

def deleteNode(request):
    return HttpResponse()

