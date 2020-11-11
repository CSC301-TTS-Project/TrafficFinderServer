from django.conf import settings
import boto3
import pickle
import copy
import uuid

# Change with config later
_DDB_ROUTE_TABLE_NAME = 'trafficfinder-route-dev'
_DDB_SEGMENT_TABLE_NAME = 'trafficfinder-sequence-dev'
_ddb = None
_route_table = None
_sequence_table = None


def _get_ddb():
    global _ddb
    if not _ddb:
        _ddb = boto3.resource('dynamodb', endpoint_url=settings.DDB_ENDPOINT)
    return _ddb


def _get_route_table():
    global _route_table
    if not _route_table:
        try:
            _get_ddb().create_table(
                AttributeDefinitions=[
                    {
                        'AttributeName': 'UserId',
                        'AttributeType': 'S',
                    },
                    {
                        'AttributeName': 'Route',
                        'AttributeType': 'N',
                    },
                    {
                        'AttributeName': 'SegmentIds',
                        'AttributeType': 'L'
                    },
                ],
                KeySchema=[
                    {
                        'AttributeName': 'UserId',
                        'KeyType': 'HASH',
                    },
                    {
                        'AttributeName': 'Route',
                        'KeyType': 'RANGE',
                    },
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5,
                },
                TableName=_DDB_ROUTE_TABLE_NAME,
            )
        finally:
            _route_table = _get_ddb().Table(_DDB_ROUTE_TABLE_NAME)
            _route_table.wait_until_exists()
    return _route_table


def _get_segment_table():
    global _sequence_table
    if not _sequence_table:
        try:
            _get_ddb().create_table(
                AttributeDefinitions=[
                    {
                        'AttributeName': 'SegmentId',
                        'AttributeType': 'S'
                    },
                    {
                        'AttributeName': 'Segment',
                        'AttributeType': 'L'
                    }
                ],
                KeySchema=[
                    {
                        'AttributeName': 'SegmentId',
                        'KeyType': 'HASH'
                    }
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5,
                },
                TableName=_DDB_SEGMENT_TABLE_NAME,
            )
        finally:
            _sequence_table = _get_ddb().Table(_DDB_SEGMENT_TABLE_NAME)
            _sequence_table.wait_until_exists()
    return _sequence_table


def get_route_segment_ids(user_id, route):
    """
    Get an ordered list of segment ids pertaining to the passed route for the given user.

    @param user_id: user id of the passed route
    @param route: id of the route
    @return: ordered list of segment ids
    """
    response = _get_route_table().get_item(Key={'UserId': user_id, 'Route': route}, ConsistentRead=True)
    if "Item" in response.keys():
        return response['Item']['SegmentIds']
    return []


def get_route_segments(segment_ids):
    """
    Get an ordered list of segments given a list of segment ids
    @param segment_ids: a list of segment ids
    @return: ordered list of segments
    """
    # make sure table is active
    _get_ddb().Table(_DDB_SEGMENT_TABLE_NAME).wait_until_exists()

    # batch_get_items doesn't guarantee order. Index segments to a dict first
    segments = {}
    unprocessed_keys = copy.deepcopy(segment_ids)
    while len(unprocessed_keys) > 0:
        response = _get_ddb().batch_get_item(
            RequestItems={
                _DDB_SEGMENT_TABLE_NAME: {
                    'Keys': [{'SegmentId': {'S': key}} for key in unprocessed_keys],
                    'ConsistentRead': True
                }
            }
        )
        if "UnprocessedKeys" in response.keys():
            unprocessed_keys = copy.deepcopy(response["UnprocessedKeys"][_DDB_SEGMENT_TABLE_NAME]["Keys"])
        for item in response["Responses"][_DDB_SEGMENT_TABLE_NAME]:
            segments[item["SegmentId"]] = [pickle.loads(node) for node in item["Segment"]]
    return [segments[segment_id] for segment_id in segment_ids]


def insert_segment_in_route_record(user_id, index, route, nodes):
    new_segment_id = str(uuid.uuid4())
    _get_segment_table().put_item(
        Item={
            'SegmentId': new_segment_id,
            'Segment:': set([pickle.dumps(node) for node in nodes])
        }
    )
    new_segment_list = get_route_segment_ids(user_id, route)
    new_segment_list.insert(index, new_segment_id)
    _get_route_table().update_item(
        Key={
            'UserId': user_id,
            'Route': route
        },
        AttributeUpdates={
            'SegmentIds': new_segment_list
        }
    )


def update_segment_in_route_record(user_id, route, index, nodes):
    new_segment_id = str(uuid.uuid4())

    _get_segment_table().put_item(
        Item={
            'SegmentId': new_segment_id,
            'Segment:': set([pickle.dumps(node) for node in nodes])
        }
    )

    new_segment_list = get_route_segment_ids(user_id, route)
    old_segment_id = new_segment_list[index]
    new_segment_list[index] = new_segment_id
    _get_route_table().update_item(
        Key={
            'UserId': user_id,
            'Route': route
        },
        AttributeUpdates={
            'SegmentIds': new_segment_list
        }
    )

    # delete old segment id
    _get_segment_table().delete_item(
        Key={
            'SegmentId': old_segment_id
        }
    )


def delete_segment_from_route_record(user_id, route, index):
    segment_list = get_route_segment_ids(user_id, route)
    segment_id_to_remove = segment_list.pop(index)

    _get_segment_table().delete_item(
        Key={
            'SegmentId': segment_id_to_remove
        }
    )
