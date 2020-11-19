import itertools

from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError, JsonResponse
import json
from .ddb_actions import get_route_segments, get_route_segment_ids, insert_route_segment, \
    update_route_segment, delete_route_segment
from django.conf import settings
from api.models import Node, Segment, TravelTime
import logging

# Set this in config, should be set using auth header later
USER = settings.DEFAULT_DDB_USER_ID

log = logging.getLogger(__name__)


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
        return JsonResponse([segment.to_json() for segment in route_segments], safe=False)
    except KeyError as e:
        log.error(f"Got the following error during get_route {e}")
        return HttpResponseBadRequest("Malformed Input")


def insert_node(request):
    try:
        json_data = json.loads(request.body)
        print(json_data)
        route = int(json_data["route"])
        lat = float(json_data["lat"])
        lng = float(json_data["lng"])
        segment_idx = json_data["index"]
        new_node = Node.objects.nearest_node(lat, lng)

        ret_json = {}
        if segment_idx == 0:
            new_segment = Segment.singular(new_node)
            insert_route_segment(USER, route, segment_idx, new_segment)
            ret_json[segment_idx] = new_segment.to_json()
            return JsonResponse(ret_json, safe=False)
        else:
            # route to new node
            segment_ids = get_route_segment_ids(USER, route)

            if not 0 <= segment_idx < len(segment_ids) + 1:
                return HttpResponseBadRequest(f"Passed index {segment_idx} out of bounds.")
            prev_node_segment = get_route_segments(
                [segment_ids[segment_idx - 1]])[0]
            prev_node = prev_node_segment.end_node
            new_segment = Segment.route_segment_between_nodes(
                prev_node, new_node)
            ret_json[segment_idx] = new_segment.to_json()
            if segment_idx + 1 < len(segment_ids):
                # update successor segment
                successor_node_segment = get_route_segments(
                    [segment_ids[segment_idx + 1]])[0]
                successor_node = successor_node_segment.end_node
                new_successor_segment = Segment.route_segment_between_nodes(
                    new_node, successor_node)
                update_route_segment(
                    USER, route, segment_idx + 1, new_successor_segment)
                ret_json[segment_idx + 1] = new_successor_segment.to_json()
            insert_route_segment(USER, route, segment_idx, new_segment)
        return JsonResponse(ret_json, safe=False)
    except (KeyError, ValueError) as e:
        log.error(e)
        return HttpResponseBadRequest("Malformed Input")


def modify_node(request):
    try:
        json_data = json.loads(request.body)
        route = json_data["route"]
        segment_idx = int(json_data["index"])
        lat = float(json_data["lat"])
        lng = float(json_data["lng"])
        segment_ids = get_route_segment_ids(USER, route)
        if not 0 <= segment_idx < len(segment_ids):
            return HttpResponseBadRequest(f"Passed segment_idx {segment_idx} out of bounds.")
        new_node = Node.objects.nearest_node(lat, lng)
        ret_json = {}
        if segment_idx - 1 >= 0:
            # There is a prev segment. Route from prev node to new node
            prev_node_segment = get_route_segments(
                [segment_ids[segment_idx - 1]])[0]
            prev_node = prev_node_segment.end_node
            modified_segment = Segment.route_segment_between_nodes(
                prev_node, new_node)
            update_route_segment(
                USER, route, segment_idx, modified_segment)
        else:
            # This is the first node.
            modified_segment = Segment.singular(new_node)
            update_route_segment(USER, route, segment_idx,
                                 modified_segment)
        ret_json[segment_idx] = modified_segment.to_json()

        if segment_idx + 1 < len(segment_ids):
            # There is a next segment. Route from new node to next node.
            successor_node_segment = get_route_segments(
                [segment_ids[segment_idx + 1]])[0]
            successor_node = successor_node_segment.end_node
            new_successor_segment = Segment.route_segment_between_nodes(
                new_node, successor_node)
            update_route_segment(USER, route, segment_idx,
                                 new_successor_segment)
            ret_json[segment_idx + 1] = new_successor_segment.to_json()

        # return any edits.
        return JsonResponse(ret_json, safe=False)

    except (KeyError, ValueError) as e:
        print(e)
        log.error(e)
        return HttpResponseBadRequest("Malformed Input")


def delete_node(request):
    # TODO: After node deletion, update indices to match
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
            prev_node_segment = get_route_segments(
                [segment_ids[segment_idx - 1]])[0]
            prev_node = prev_node_segment.end_node

            successor_node_segment = get_route_segments(
                [segment_ids[segment_idx + 1]])[0]
            successor_node = successor_node_segment.end_node

            new_successor_segment = Segment.route_segment_between_nodes(
                prev_node, successor_node)
            update_route_segment(
                USER, route, segment_idx + 1, new_successor_segment)
            ret_json[segment_idx] = new_successor_segment.to_json()
        elif segment_idx + 1 < len(segment_ids):
            # deleting first node
            successor_node_segment = get_route_segments(
                [segment_ids[segment_idx + 1]])[0]
            successor_node = successor_node_segment.end_node
            new_starting_segment = Segment.singular(successor_node)
            update_route_segment(USER, route, segment_idx,
                                 new_starting_segment)
            ret_json[segment_idx] = new_starting_segment.to_json()
        # otherwise, don't need to send back updates since it was the last node segment that was deleted
        delete_route_segment(USER, route, segment_idx)
        return JsonResponse(ret_json, safe=False)
    except (KeyError, ValueError) as e:
        print(e)
        log.error(e)
        return HttpResponseBadRequest("Malformed Input")


def get_traffic_data(request):
    """
    Get traffic data in csv format.

    Will later support optional fields.

    Expects a json body with the following parameters:
        route: the corresponding route you are fetching data for
        date_range: the date range to query
        days_of_week: the days of the week to query in integer format,
            i.e. [0, 2, 4] corresponds to [Sunday, Tuesday, Thursday]
        hour_range: the hour range to query

    @return: csv body with hourly aggregated traffic data for the time window
    """
    log.debug("Received [GET] getTrafficData")
    try:
        json_data = json.loads(request.body)
        route = int(json_data["route"])
        date_range = json_data["date_range"]
        days_of_week = [int(day) for day in json_data["days_of_week"]]
        hour_range = [int(hr) for hr in json_data["hour_range"]]
        route_segment_ids = get_route_segment_ids(USER, route)
        route_segments = get_route_segments(route_segment_ids)

        route_here_data = TravelTime.get_data_for_route(
            list(itertools.chain.from_iterable(
                [seg.link_dirs for seg in route_segments])), date_range, days_of_week,
            hour_range)

        response_csv = ",".join(route_here_data[0].keys())
        response_csv += '\n'
        for record in route_here_data:
            response_csv += ",".join([str(val) for val in record.values()])
            response_csv += '\n'
        return HttpResponse(response_csv, content_type='text/csv')
    except KeyError as e:
        log.error(f"Got the following error during getTrafficData {e}")
        return HttpResponseBadRequest("Malformed Input")
