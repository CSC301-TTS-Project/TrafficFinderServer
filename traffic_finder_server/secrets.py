import boto3
from botocore.exceptions import ClientError
import json


def get_secrets_dict():
    secret_name = "TrafficFinder/API"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager'
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e
    else:
        secret_dict = json.loads(get_secret_value_response['SecretString'])
        return secret_dict
