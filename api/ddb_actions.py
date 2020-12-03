import pickle
import copy
import uuid
from django.conf import settings
import boto3

# Change with config later
_DDB_ROUTE_TABLE_NAME = settings.DDB_ROUTE_TABLE_NAME
_DDB_SEGMENT_TABLE_NAME = settings.DDB_SEGMENT_TABLE_NAME

_DDB = None
_ROUTE_TABLE = None
_SEQUENCE_TABLE = None


def _get_ddb():
    """Get the DynamoDB table from the Database endpoint"""
    global _DDB
    if not _DDB:
        _DDB = boto3.resource('dynamodb', endpoint_url=settings.DDB_ENDPOINT)
    return _DDB


def _get_route_table(reset_table=False):
    """
    Initialize the routing table if does not exist
    otherwise return table with required attributes
    """
    global _ROUTE_TABLE
    if not _ROUTE_TABLE or reset_table:
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
                    }
                ],
                KeySchema=[
                    {
                        'AttributeName': 'UserId',
                        'KeyType': 'HASH',
                    },
                    {
                        'AttributeName': 'Route',
                        'KeyType': 'RANGE',
                    }
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5,
                },
                TableName=_DDB_ROUTE_TABLE_NAME,
            )
        except _get_ddb().meta.client.exceptions.ResourceInUseException:
            # table has already been created
            pass
        finally:
            _ROUTE_TABLE = _get_ddb().Table(_DDB_ROUTE_TABLE_NAME)
            _ROUTE_TABLE.wait_until_exists()

            # initialize default route; implementation will change for
            # deliverable 3
            _ROUTE_TABLE.put_item(
                Item={
                    "UserId": settings.DEFAULT_DDB_USER_ID,
                    "Route": settings.DEFAULT_ROUTE,
                    "SegmentIds": []
                }
            )
        return _ROUTE_TABLE


def _get_segment_table(reset_table=False):
    global _SEQUENCE_TABLE
    if not _SEQUENCE_TABLE or reset_table:
        try:
            _get_ddb().create_table(
                AttributeDefinitions=[
                    {
                        'AttributeName': 'SegmentId',
                        'AttributeType': 'S'
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
                    'WriteCapacityUnits': 5
                },
                TableName=_DDB_SEGMENT_TABLE_NAME,
            )
        except _get_ddb().meta.client.exceptions.ResourceInUseException:
            # table has already been created
            pass
        finally:
            _SEQUENCE_TABLE = _get_ddb().Table(_DDB_SEGMENT_TABLE_NAME)
            _SEQUENCE_TABLE.wait_until_exists()
    return _SEQUENCE_TABLE


def get_route_segment_ids(user_id, route):
    """
    Get an ordered list of segment ids pertaining to the passed route for the given user.

    @param user_id: user id of the passed route
    @param route: id of the route
    @return: ordered list of segment ids
    """
    response = _get_route_table().get_item(
        Key={'UserId': user_id, 'Route': route},
        ConsistentRead=True)
    if "Item" in response.keys():
        return response['Item']['SegmentIds']
    return []


def get_route_segments(segment_ids):
    """
        Get an ordered list of segments given a list of segment ids
        @param segment_ids: a list of segment ids
        @return: ordered list of segments
        (each segment starts and ends with nodes that define the endpoints of the segment)
    """
    # make sure table is active
    _get_segment_table()
    # batch_get_items doesn't guarantee order. Index segments to a dict first
    segments = {}
    unprocessed_keys = copy.deepcopy(segment_ids)
    while len(unprocessed_keys) > 0:
        response = _get_ddb().batch_get_item(
            RequestItems={
                _DDB_SEGMENT_TABLE_NAME: {
                    'Keys': [{'SegmentId': key} for key in unprocessed_keys],
                    'ConsistentRead': True
                }
            }
        )
        unprocessed_keys.clear()
        if len(response["UnprocessedKeys"]) > 0:
            unprocessed_keys.append(
                [x['S']
                    for x in response["UnprocessedKeys"]
                    [_DDB_SEGMENT_TABLE_NAME]["Keys"]])
        for item in response["Responses"][_DDB_SEGMENT_TABLE_NAME]:
            segments[item["SegmentId"]] = pickle.loads(item["Segment"].value)
    return [segments[segment_id] for segment_id in segment_ids]


def insert_route_segment(user_id, route, index, segment):
    """
    Add a new segment to the given route
    @param user_id: user id of the passed route
    @param route: id of the route
    @param index: index of the segment in route
    @param segment: the segment to insert
    """
    new_segment_id = str(uuid.uuid4())
    _get_segment_table().put_item(
        Item={
            'SegmentId': new_segment_id,
            'Segment': pickle.dumps(segment)
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
            'SegmentIds': {'Value': new_segment_list}
        }
    )


def update_route_segment(user_id, route, index, segment):
    """
    Update a segment in the given route
    @param user_id: user id of the passed route
    @param route: id of the route
    @param index: index of the segment in route
    @param segment: the segment to insert
    """
    new_segment_id = str(uuid.uuid4())

    _get_segment_table().put_item(
        Item={
            'SegmentId': new_segment_id,
            'Segment': pickle.dumps(segment)
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
            'SegmentIds': {'Value': new_segment_list}
        }
    )

    # delete old segment id
    _get_segment_table().delete_item(
        Key={
            'SegmentId': old_segment_id
        }
    )


def delete_route_segment(user_id, route, index):
    """
    Delete a segment from the given route
    @param user_id: user id of the passed route
    @param route: id of the route
    @param index: index of the segment in route
    """
    segment_list = get_route_segment_ids(user_id, route)
    segment_id_to_remove = segment_list.pop(index)

    _get_segment_table().delete_item(
        Key={
            'SegmentId': segment_id_to_remove
        }
    )

    _get_route_table().update_item(
        Key={
            'UserId': user_id,
            'Route': route
        },
        AttributeUpdates={
            'SegmentIds': {'Value': segment_list}
        }
    )


def reset():
    """
    Reset Segment and route table
    """
    _get_segment_table(reset_table=True)
    _get_route_table(reset_table=True)
