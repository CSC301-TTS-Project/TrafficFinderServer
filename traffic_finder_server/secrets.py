import boto3
from botocore.exceptions import ClientError
import json
import os


def load_secrets_env():
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

        for key, value in secret_dict.items():
            os.environ['key'] = value


if __name__ == '__main__':
    load_secrets_env()
