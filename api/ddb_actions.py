from django.conf import settings
import boto3

#Change with config later
_DDB_TABLE_NAME = 'trafficfinder-dev'
_ddb = None
_table = None

def _get_ddb():
    if not _ddb: 
        _ddb = boto3.resource('dynamodb', endpoint_url=settings.DDB_ENDPOINT)
    return _ddb

def _get_table():
    if not _table:
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
                TableName = _DDB_TABLE_NAME,
            )
        finally:
            table = _get_ddb().Table(_DDB_TABLE_NAME)
            table.wait_until_exists()
    return table

def get_route_record(user_id, route):
    raise NotImplementedError

def update_route_record(user_id, route, node_dict):
    raise NotImplementedError

