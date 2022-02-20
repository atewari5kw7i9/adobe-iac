import boto3
from datetime import datetime
from urllib.parse import unquote_plus
import os
import json

def lambda_handler(event, context):

    bucket_name_src = event["Records"][0]["s3"]["bucket"]["name"]
    s3_file_name_src = unquote_plus(event["Records"][0]["s3"]["object"]["key"])
    todays_dt = datetime.today().strftime('%Y-%m-%d')

    s3 = boto3.resource('s3')
    copy_source = {
        'Bucket': bucket_name_src,
        'Key': s3_file_name_src
    }

    output_bucket = os.environ["output_bucket"]
    output_prefix = os.environ["output_prefix"]
    sns_arn = os.environ["sns_arn"]
    destination_key_name = "{}/{}_{}".format(output_prefix, todays_dt, "SearchKeywordPerformance.tab")
    s3.meta.client.copy(copy_source, output_bucket, destination_key_name)
    resp = {"status": 0, "Desc": destination_key_name + " file copied successfully"}
    client = boto3.client('sns')
    response = client.publish(
        TargetArn=sns_arn,
        Message=json.dumps(resp)
    )
    return resp
