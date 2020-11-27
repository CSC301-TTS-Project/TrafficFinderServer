import json
import boto3
from botocore.exceptions import ClientError


def get_secrets_dict():
    """
    Get AWS Secret Manager secrets for our application
    @return: a dictionary that maps keys to secrets
    """
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
    except ClientError as error:
        raise error
    else:
        secret_dict = json.loads(get_secret_value_response['SecretString'])
        return secret_dict
