import itertools

from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError, JsonResponse
import json
from .ddb_actions import get_route_segments, get_route_segment_ids, insert_route_segment, \
    update_route_segment, delete_route_segment
from django.conf import settings
from api.models import Node, Segment, TravelTime
import logging
from .api_keys import api_keys_dict
import traceback

# Set this in config, should be set using auth header later
USER = settings.DEFAULT_DDB_USER_ID

log = logging.getLogger(__name__)


def index(request):
    return HttpResponse("Hello World!")


def get_route(request):
    """ Expect the json field route """
    log.debug("Received [POST] get_route")
    try:
        json_data = json.loads(request.body)
        route = int(json_data["route"])
        route_segment_ids = get_route_segment_ids(USER, route)
        route_segments = get_route_segments(route_segment_ids)
        return JsonResponse([segment.to_json()
                             for segment in route_segments], safe=False)
    except KeyError as e:
        log.error(
            f"Got the following error during get_route: {traceback.format_exc()}")
        return HttpResponseBadRequest("Malformed Input")


def insert_node(request):
    """
    Insert segment into a route

    This expects a json body with the following parameters:
        route: The index of the route to insert into
        lat: The latitude of the endpoint of new segment
        lng: The longitude of the endpoint of new segment
        index: The segment ID of the new segment to be created     
    """
    try:
        log.debug("Received [POST] insert_node")
        json_data = json.loads(request.body)
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
                return HttpResponseBadRequest(
                    f"Passed index {segment_idx} out of bounds.")
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
        log.error(
            f"Got the following error during insert_node: {traceback.format_exc()}")
        return HttpResponseBadRequest("Malformed Input")


def modify_node(request):
    """
    Modify segment in a route

    This expects a json body with the following parameters:
        route: The index of the route to modify
        lat: The latitude of the endpoint of edited segment
        lng: The longitude of the endpoint of edited segment
        index: The segment ID of the segment to be edited     
    """
    try:
        log.debug("Received [POST] modify_node")
        json_data = json.loads(request.body)
        route = json_data["route"]
        segment_idx = int(json_data["index"])
        lat = float(json_data["lat"])
        lng = float(json_data["lng"])
        segment_ids = get_route_segment_ids(USER, route)
        if not 0 <= segment_idx < len(segment_ids):
            return HttpResponseBadRequest(
                f"Passed segment_idx {segment_idx} out of bounds.")
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
        log.error(
            f"Got the following error during modify_node: {traceback.format_exc()}")
        return HttpResponseBadRequest("Malformed Input")


def delete_node(request):
    """
    Delete segment in a route

    This expects a json body with the following parameters:
        route: The index of the route to edited
        index: The segment ID of the segment to be deleted     
    """
    try:
        log.debug("Received [DELETE] delete_node")
        json_data = json.loads(request.body)
        route = json_data["route"]
        segment_idx = json_data["index"]

        segment_ids = get_route_segment_ids(USER, route)
        if not 0 <= segment_idx < len(segment_ids):
            return HttpResponseBadRequest(
                f"Passed segment_idx {segment_idx} out of bounds.")

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
            update_route_segment(
                USER, route, segment_idx + 1, new_starting_segment)
            ret_json[segment_idx] = new_starting_segment.to_json()
        # otherwise, don't need to send back updates since it was the last node
        # segment that was deleted
        delete_route_segment(USER, route, segment_idx)
        return JsonResponse(ret_json, safe=False)
    except (KeyError, ValueError) as e:
        log.error(
            f"Got the following error during delete_node: {traceback.format_exc()}")
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
    log.debug("Received [POST] getTrafficData")
    try:
        json_data = json.loads(request.body)
        route = int(json_data["route"])
        date_range = json_data["date_range"]
        days_of_week = [int(day) for day in json_data["days_of_week"]]
        hour_range = [int(hr) for hr in json_data["hour_range"]]
        selections = [int(select) for select in json_data["selections"]]

        route_segment_ids = get_route_segment_ids(USER, route)
        route_segments = get_route_segments(route_segment_ids)

        links_dirs_list = list(itertools.chain.from_iterable(
            [seg.link_dirs for seg in route_segments]))
        if len(links_dirs_list) <= 0:
            return HttpResponse("No route data to fetch.")
        log.debug(links_dirs_list)

        route_here_data = TravelTime.get_data_for_route(
            links_dirs_list, date_range, days_of_week,
            hour_range)
        log.debug(route_here_data)
        wanted_data = []
        for i, key in enumerate(route_here_data[0].keys()):
            if selections[i]:
                wanted_data.append(key)
        response_csv = ",".join(wanted_data)
        response_csv += '\n'
        for record in route_here_data:
            wanted_vals = []
            keys = record.keys()
            for key in keys:
                if key in wanted_data:
                    wanted_vals.append(record[key])
            response_csv += ",".join([str(val) for val in wanted_vals])
            response_csv += '\n'
        return HttpResponse(response_csv, content_type='text/csv')
    except KeyError as e:
        log.error(
            f"Got the following error during getTrafficData: {traceback.format_exc()}")
        return HttpResponseBadRequest("Malformed Input")


def get_api_keys(request):
    return JsonResponse(api_keys_dict(), safe=False)
