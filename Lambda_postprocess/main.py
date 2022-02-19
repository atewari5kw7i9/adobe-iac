import boto3
from os.path import join
import uuid
import os
from urllib.parse import unquote_plus


def lambda_handler(event, context):

    bucket_name_src = event["Records"][0]["s3"]["bucket"]["name"]
    s3_file_name_src = unquote_plus(event["Records"][0]["s3"]["object"]["key"])
    input_path = "{}/{}".format(bucket_name_src, s3_file_name_src)
    return input_path
