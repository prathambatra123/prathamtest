import boto3
import os
from botocore.exceptions import ClientError


def get_client(serv , region_name='us-eat-1'):
    session = boto3.Session(profile_name=os.environ["creds_profile"])
    return session.client(serv,region_name=region_name)