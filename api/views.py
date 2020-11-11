from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError, JsonResponse
import json
from .ddb_actions import get_route_segments, get_route_segment_ids, insert_route_segment, \
    update_route_segment, delete_route_segment
from .pg_routing_queries import shortest_route, nearest_node
from django.conf import settings
import logging

# Set this in config, should be set using auth header later
USER = settings.DEFAULT_DDB_USER_ID

log = logging.getLogger(__name__)
logging.disable(logging.NOTSET)
log.setLevel(logging.DEBUG)

def index(request):
    return HttpResponse("Hello World!")


def get_route(request):
    """ Expect the json field route """
    log.debug("Received [GET] get_route")
    try:
        json_data = json.loads(request.body)
        route = int(json_data["route"])
        route_segment_ids = get_route_segment_ids(USER, route)
        route_segments = get_route_segments(route_segment_ids)
        return JsonResponse(json.dumps(route_segments), safe=False)
    except KeyError as e:
        log.error(f"Got the following error during get_route {e}")
        return HttpResponseBadRequest("Malformed Input")


def insert_node(request):
    try:
        json_data = json.loads(request.body)
        route = int(json_data["route"])
        lat = float(json_data["lat"])
        lng = float(json_data["lng"])
        segment_idx = json_data["index"]
        new_node = nearest_node(lat, lng)
        if segment_idx == 0:
            insert_route_segment(USER, route, segment_idx, [new_node])
            return JsonResponse(json.dumps(new_node))
        else:
            # route to new node
            segment_ids = get_route_segment_ids(USER, route)
            if not 0 <= segment_idx < len(segment_ids):
                return HttpResponseBadRequest(f"Passed segment_idx {segment_idx} out of bounds.")

            prev_node_segment = get_route_segments([segment_ids[segment_idx - 1]])[0]
            prev_node = prev_node_segment[-1]
            new_segment = shortest_route(prev_node, new_node)
            ret_json = {segment_idx: new_segment}
            if segment_idx + 1 < len(segment_ids):
                # update successor segment
                successor_node_segment = get_route_segments([segment_ids[segment_idx + 1]])[0]
                successor_node = successor_node_segment[-1]
                new_successor_segment = shortest_route(new_node, successor_node)
                update_route_segment(USER, route, segment_idx + 1, new_successor_segment)
                ret_json[segment_idx + 1] = new_successor_segment
            insert_route_segment(USER, route, segment_idx, new_segment)
            return JsonResponse(ret_json, safe=False)
    except (KeyError, ValueError):
        return HttpResponseBadRequest("Malformed Input")


def modify_node(request):
    return HttpResponse()


def delete_node(request):
    try:
        json_data = json.loads(request.body)
        route = json_data["route"]
        segment_idx = json_data["index"]

        segment_ids = get_route_segment_ids(USER, route)
        if not 0 <= segment_idx < len(segment_ids):
            return HttpResponseBadRequest(f"Passed segment_idx {segment_idx} out of bounds.")

        ret_json = {}
        if segment_idx - 1 >= 0 and segment_idx + 1 < len(segment_ids):
            # deleting an intermediate segment
            prev_node_segment = get_route_segments([segment_ids[segment_idx - 1]])[0]
            prev_node = prev_node_segment[-1]

            successor_node_segment = get_route_segments([segment_ids[segment_idx + 1]])[0]
            successor_node = successor_node_segment[-1]

            new_successor_segment = shortest_route(prev_node, successor_node)
            update_route_segment(USER, route, segment_idx + 1, new_successor_segment)
            ret_json[segment_idx] = new_successor_segment
        elif segment_idx + 1 < len(segment_ids):
            # deleting first node
            successor_node_segment = get_route_segments([segment_ids[segment_idx + 1]])[0]
            successor_node = successor_node_segment[-1]
            update_route_segment(USER, route, segment_idx, [successor_node])
            ret_json[segment_idx] = [successor_node]
        # otherwise, don't need to send back updates since it was the last node segment that was deleted
        delete_route_segment(USER, route, segment_idx)
        return JsonResponse(ret_json, safe=False)
    except (KeyError, ValueError):
        return HttpResponseBadRequest("Malformed Input")


# HARD CODED VARIANTS BELOW
# =======================DELETE ALL OF BELOW IN FINAL==========================


def hdc_index(request):
    return HttpResponse("Hello World!")


def hdc_getRoute(request):
    """ Expect the json fields route. """
    json_data = json.loads(request.body)
    try:
        route = json_data["route"]
        return JsonResponse(json.dumps({"KEY": "Value"}), safe=False)
    except KeyError:
        return HttpResponseBadRequest("Malformed Input")


def hdc_insertNode(request):
    json_data = json.loads(request.body)
    try:
        route = json_data["route"]
        lat = json_data["lat"]
        lng = json_data["lng"]
        segment_idx = json_data["index"]
        return JsonResponse(json.dumps({"KEY": "Value"}), safe=False)
    except KeyError:
        return HttpResponseBadRequest("Malformed Input")


def hdc_modifyNode(request):
    return HttpResponse("Modified Node")


def hdc_deleteNode(request):
    json_data = json.loads(request.body)
    try:
        route = json_data["route"]
        segment_idx = json_data["index"]
        return JsonResponse(json.dumps({"KEY": "Value"}), safe=False)
    except KeyError:
        return HttpResponseBadRequest("Malformed Input")


def hdc_addNodeToRoute(request):
    json_data = json.loads(request.body)
    try:
        route = json_data["route"]
        segment_idx = json_data["index"]
        lat = json_data["lat"]
        lng = json_data["lng"]
        assert isinstance(lat, float) and isinstance(lng, float) and isinstance(
            segment_idx, int) and isinstance(route, int)
        return JsonResponse(json.dumps(
            [{"id": 123, "lat": 43.651072, "lng": -79.347016}, {"id": 12, "lat": 43.651070, "lng": -79.347015},
             {"id": 17, "lat": lat, "lng": lng}]), safe=False)
    except (KeyError, AssertionError):
        return HttpResponseBadRequest("Malformed Input.\nPlease Use JSON keys: route, index, lat, lng")


def hdc_modifyRouteNode(request):
    json_data = json.loads(request.body)
    try:
        route = json_data["route"]
        segment_idx = json_data["index"]
        lat = json_data["lat"]
        lng = json_data["lng"]
        assert isinstance(lat, float) and isinstance(lng, float) and isinstance(
            segment_idx, int) and isinstance(route, int)
        return JsonResponse(json.dumps([{"index": 1, "id": 123, "lat": 43.651072, "lng": -79.347016},
                                        {"index": 2, "id": 12, "lat": 43.651070, "lng": -79.347015},
                                        {"index": 3, "id": 17, "lat": lat, "lng": lng}]), safe=False)
    except (KeyError, AssertionError):
        return HttpResponseBadRequest("Malformed Input.\nPlease Use JSON keys: route, index, lat, lng")


def hdc_deleteRouteNode(request):
    json_data = json.loads(request.body)
    try:
        route = json_data["route"]
        segment_idx = json_data["index"]
        assert isinstance(segment_idx, int) and isinstance(route, int)
        return JsonResponse(json.dumps([{"index": 1, "id": 123, "lat": 43.651072, "lng": -79.347016},
                                        {"index": 2, "id": 12, "lat": 43.651070, "lng": -79.347015}]), safe=False)
    except (KeyError, AssertionError):
        return HttpResponseBadRequest("Malformed Input.\nPlease Use JSON keys: route, index")


def hdc_getTrafficData(request):
    json_data = json.loads(request.body)
    try:
        route = json_data["route"]
        assert isinstance(route, int)
        return HttpResponse("0, 1, 2, 3, 4, 5\n6, 7, 8, 9, 10, 11\n12, 13, 14, 15, 16, 17, 18")
    except (KeyError, AssertionError):
        return HttpResponseBadRequest("Malformed Input")
