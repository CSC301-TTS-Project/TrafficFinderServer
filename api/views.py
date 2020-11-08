from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError, JsonResponse
import json
from .ddb_actions import get_route_record, update_route_record, get_segment
from .pg_routing_queries import shortest_route, nearest_node

# Set this in config, should be set using auth header later
USER = 'user'


def index(request):
    return HttpResponse("Hello World!")


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
            # route to new node
            prev_node_segment = get_segment(USER, route, segment_idx - 1)
            prev_nodes_len = prev_node_segment[f"segment_{segment_idx - 1}_length"]
            prev_node = prev_node_segment[f"segment_{segment_idx - 1}"][prev_nodes_len - 1]
            new_segment = shortest_route(prev_node, new_node)
            update_route_record(USER, route, segment_idx, new_segment)

            ret_json = {segment_idx: json.dumps(new_segment)}

            # new node to existing successor node
            next_node_segment = get_segment(USER, route, segment_idx + 1)

            # TODO: Need to change function behavior to return null on non-existing segment idx
            if next_node_segment:
                next_nodes_len = next_node_segment[f"segment_{segment_idx + 1}_length"]
                successor_node = next_node_segment[next_nodes_len - 1]
                new_successor_segment = shortest_route(
                    new_node, successor_node)
                update_route_record(
                    USER, route, segment_idx + 1, new_successor_segment)
                ret_json[segment_idx + 1] = json.dumps(new_successor_segment)
            return JsonResponse(json.dumps(ret_json))
    except KeyError:
        return HttpResponseBadRequest("Malformed Input")


def modifyNode(request):
    return HttpResponse()


def deleteNode(request):
    json_data = json.loads(request.body)
    try:
        route = json_data["route"]
        segment_idx = json_data["index"]
        update_route_record(USER, route, segment_idx, None, delete=True)

        next_node_segment = get_segment(USER, route, segment_idx)
        prev_node_segment = get_segment(USER, route, segment_idx - 1)
        ret_json = {}
        if next_node_segment and prev_node_segment:
            # deleting an intermediate segment
            next_nodes_len = next_node_segment[f"segment_{segment_idx}_length"]
            successor_node = next_node_segment[next_nodes_len - 1]

            prev_nodes_len = prev_node_segment[f"segment_{segment_idx - 1}_length"]
            prev_node = prev_node_segment[f"segment_{segment_idx - 1}"][prev_nodes_len - 1]

            new_successor_segment = shortest_route(prev_node, successor_node)
            update_route_record(USER, route, segment_idx,
                                new_successor_segment)
            ret_json[segment_idx] = json.dumps(new_successor_segment)
        elif next_node_segment:
            next_nodes_len = next_node_segment[f"segment_{segment_idx}_length"]
            successor_node = next_node_segment[next_nodes_len - 1]
            update_route_record(USER, route, segment_idx, successor_node)
            ret_json[segment_idx] = json.dumps(successor_node)
        # otherwise, don't need to send updates back since it's the last node segment that was deleted
        return JsonResponse(ret_json)
    except KeyError:
        return HttpResponseBadRequest("Malformed Input")

# HARD CODED VARIANTS BELOW


def hdc_index(request):
    return HttpResponse("Hello World!")


def hdc_getRoute(request):
    """ Expect the json fields route. """
    pass


def hdc_insertNode(request):
    json_data = json.loads(request.body)
    try:
        route = json_data["route"]
        lat = json_data["lat"]
        lng = json_data["lng"]
        segment_idx = json_data["index"]
        return JsonResponse(json.dumps(ret_json))
    except KeyError:
        return HttpResponseBadRequest("Malformed Input")


def hdc_modifyNode(request):
    return HttpResponse()


def hdc_deleteNode(request):
    json_data = json.loads(request.body)
    try:
        route = json_data["route"]
        segment_idx = json_data["index"]
        return JsonResponse(ret_json)
    except KeyError:
        return HttpResponseBadRequest("Malformed Input")
