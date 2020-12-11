from rest_framework.response import Response
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt
import itertools

from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError, JsonResponse
import json

from django.http.response import HttpResponseForbidden, HttpResponseNotAllowed
from .ddb_actions import get_route_segments, get_route_segment_ids, insert_route_segment, \
    update_route_segment, delete_route_segment, add_user_route
from django.conf import settings
from api.models import Node, Segment, TravelTime
import logging
from .api_keys import api_keys_dict
import traceback
from django.db import connection
from time import time
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

# Set this in config, should be set using auth header later
DEFAULT_ROUTE = settings.DEFAULT_ROUTE

log = logging.getLogger(__name__)
COLUMN_NAMES = "route_num,num_days,link_obs,min_speed,mean_speed,max_speed,pct_50_speed,pct_85_speed,pct_95_speed," \
               "std_dev_speed,min_tt,mean_tt,max_tt,std_dev_tt,total_length,full_link_obs".split(
                   ",")


def index(request):
    return HttpResponse("Hello World!")


@api_view(["POST"])
def get_route(request):
    """ Expect the json field route """
    log.debug("Received [POST] get_route")
    if not request.user.is_authenticated:
        return HttpResponseForbidden("User must be signed in")
    try:
        user = request.user.id
        json_data = json.loads(request.body)
        route = int(json_data["route"])
        route_segment_ids = get_route_segment_ids(user, route)
        route_segments = get_route_segments(route_segment_ids)
        return JsonResponse([segment.to_json()
                             for segment in route_segments], safe=False)
    except KeyError as e:
        log.error(
            f"Got the following error during get_route: {traceback.format_exc()}")
        return HttpResponseBadRequest("Malformed Input")


# def check(request):
#     if not request.user.is_authenticated:
#         print("User did not exist")
#         return HttpResponseForbidden("User must be signed in")
#     return HttpResponse("Success")


@api_view(["POST"])
def insert_node(request):
    """
    Insert segment into a route

    This expects a json body with the following parameters:
        route: The index of the route to insert into
        lat: The latitude of the endpoint of new segment
        lng: The longitude of the endpoint of new segment
        index: The segment ID of the new segment to be created
    """
    log.debug("Received [POST] insert_node")
    print(request.user)
    if not request.user.is_authenticated:
        print("User did not exist")
        return HttpResponseForbidden("User must be signed in")
    try:
        user = request.user.id
        json_data = json.loads(request.body)
        route = int(json_data["route"])
        lat = float(json_data["lat"])
        lng = float(json_data["lng"])
        segment_idx = json_data["index"]
        new_node = Node.objects.nearest_node(lat, lng)

        ret_json = {}
        if segment_idx == 0:
            new_segment = Segment.singular(new_node)
            insert_route_segment(user, route, segment_idx, new_segment)
            ret_json[segment_idx] = new_segment.to_json()
            return JsonResponse(ret_json, safe=False)
        else:
            # route to new node
            segment_ids = get_route_segment_ids(user, route)

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
                    user, route, segment_idx + 1, new_successor_segment)
                ret_json[segment_idx + 1] = new_successor_segment.to_json()
            insert_route_segment(user, route, segment_idx, new_segment)
        return JsonResponse(ret_json, safe=False)
    except (KeyError, ValueError) as e:
        log.error(
            f"Got the following error during insert_node: {traceback.format_exc()}")
        return HttpResponseBadRequest("Malformed Input")


@api_view(["PATCH"])
def modify_node(request):
    """
    Modify segment in a route

    This expects a json body with the following parameters:
        route: The index of the route to modify
        lat: The latitude of the endpoint of edited segment
        lng: The longitude of the endpoint of edited segment
        index: The segment ID of the segment to be edited
    """
    log.debug("Received [POST] modify_node")
    if not request.user.is_authenticated:
        return HttpResponseForbidden("User must be signed in")
    try:
        user = request.user.id
        json_data = json.loads(request.body)
        route = json_data["route"]
        segment_idx = int(json_data["index"])
        lat = float(json_data["lat"])
        lng = float(json_data["lng"])
        segment_ids = get_route_segment_ids(user, route)
        if not 0 <= segment_idx < len(segment_ids):
            return HttpResponseBadRequest(
                f"Passed segment_idx {segment_idx} out of bounds.")
        new_node = Node.objects.nearest_node(lat, lng)
        ret_json = {"new_node": new_node.to_json(), "segment_updates": {}}

        if segment_idx - 1 >= 0:
            # There is a prev segment. Route from prev node to new node
            prev_node_segment = get_route_segments(
                [segment_ids[segment_idx - 1]])[0]
            prev_node = prev_node_segment.end_node
            modified_segment = Segment.route_segment_between_nodes(
                prev_node, new_node)
            update_route_segment(
                user, route, segment_idx, modified_segment)
        else:
            # This is the first node.
            modified_segment = Segment.singular(new_node)
            update_route_segment(user, route, segment_idx, modified_segment)
        ret_json["segment_updates"][segment_idx] = modified_segment.to_json()

        if segment_idx + 1 < len(segment_ids):
            # There is a next segment. Route from new node to next node.
            successor_node_segment = get_route_segments(
                [segment_ids[segment_idx + 1]])[0]
            successor_node = successor_node_segment.end_node
            new_successor_segment = Segment.route_segment_between_nodes(
                new_node, successor_node)
            update_route_segment(user, route, segment_idx + 1,
                                 new_successor_segment)
            ret_json["segment_updates"][segment_idx +
                                        1] = new_successor_segment.to_json()

        # return any edits.
        return JsonResponse(ret_json, safe=False)

    except (KeyError, ValueError) as e:
        log.error(
            f"Got the following error during modify_node: {traceback.format_exc()}")
        return HttpResponseBadRequest("Malformed Input")


@api_view(["POST"])
def delete_node(request):
    """
    Delete segment in a route

    This expects a json body with the following parameters:
        route: The index of the route to edited
        index: The segment ID of the segment to be deleted
    """
    log.debug("Received [DELETE] delete_node")
    if not request.user.is_authenticated:
        return HttpResponseForbidden("User must be signed in")
    try:
        json_data = json.loads(request.body)
        route = json_data["route"]
        segment_idx = json_data["index"]
        user = request.user.id
        segment_ids = get_route_segment_ids(user, route)
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
                user, route, segment_idx + 1, new_successor_segment)
            ret_json[segment_idx] = new_successor_segment.to_json()
        elif segment_idx + 1 < len(segment_ids):
            # deleting first node
            successor_node_segment = get_route_segments(
                [segment_ids[segment_idx + 1]])[0]
            successor_node = successor_node_segment.end_node
            new_starting_segment = Segment.singular(successor_node)
            update_route_segment(
                user, route, segment_idx + 1, new_starting_segment)
            ret_json[segment_idx] = new_starting_segment.to_json()
        # otherwise, don't need to send back updates since it was the last node
        # segment that was deleted
        delete_route_segment(user, route, segment_idx)
        return JsonResponse(ret_json, safe=False)
    except (KeyError, ValueError) as e:
        log.error(
            f"Got the following error during delete_node: {traceback.format_exc()}")
        return HttpResponseBadRequest("Malformed Input")


@api_view(["POST"])
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
    if not request.user.is_authenticated:
        return HttpResponseForbidden("User must be signed in")
    try:
        json_data = json.loads(request.body)
        route = int(json_data["route"])
        date_range = json_data["date_range"]
        days_of_week = [int(day) for day in json_data["days_of_week"]]
        hour_range = [int(hr) for hr in json_data["hour_range"]]
        selections = [int(select) for select in json_data["selections"]]
        user = request.user.id

        wanted_data = []

        start = time()
        for i in range(len(selections)):
            if selections[i]:
                wanted_data.append(COLUMN_NAMES[i])
        end = time()
        print("Views 238: ", end - start)

        start = time()
        route_segment_ids = get_route_segment_ids(user, route)
        route_segments = get_route_segments(route_segment_ids)
        end = time()
        print("Views 245: ", end - start)

        start = time()
        links_dirs_list = list(itertools.chain.from_iterable(
            [seg.link_dirs for seg in route_segments]))
        if len(links_dirs_list) <= 0:
            return HttpResponse("No route data to fetch.")
        end = time()
        print("Views 251: ", end - start)

        start = time()
        route_here_data = TravelTime.get_data_for_route(route,
                                                        links_dirs_list, date_range, days_of_week,
                                                        hour_range)
        end = time()
        print("Views 259: : ", end - start)

        start = time()
        response_csv = ",".join(wanted_data) + "\n"
        end = time()
        print("Views 267: ", end - start)

        print("Length of route: ", len(route_here_data))
        start = time()
        response_csv += ",".join([str(route_here_data[key])
                                  for key in wanted_data])
        response_csv += '\n'
        # response = qs_to_csv_response(route_here_data)
        end = time()
        print("Views 268: ", end - start)
        # return response
        return HttpResponse(response_csv, content_type='text/csv')

    except KeyError as e:
        log.error(
            f"Got the following error during getTrafficData: {traceback.format_exc()}")
        return HttpResponseBadRequest("Malformed Input")


@api_view(["GET"])
def get_api_keys(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden("User must be signed in")
    return JsonResponse(api_keys_dict(), safe=False)


@csrf_exempt
def login_user(request):
    try:
        username = request.POST['username']
        password = request.POST['password']
        print(username)
        print(password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse("Login Success")
        else:
            return HttpResponseNotAllowed("User Does Not Exist")
    except (KeyError, ValueError) as e:
        log.error(
            f"Got the following error during login_user: {traceback.format_exc()}")
        return HttpResponseBadRequest("Malformed Input")


@csrf_exempt
def signup_user(request):
    try:
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        user = User.objects.create_user(username, email, password)
        token = Token.objects.create(user=user)
        add_user_route(user.id, DEFAULT_ROUTE)
        return JsonResponse({'token': token.key}, safe=False)
    except (KeyError, ValueError) as e:
        log.error(
            f"Got the following error during signup_user: {traceback.format_exc()}")
        return HttpResponseBadRequest("Malformed Input")
