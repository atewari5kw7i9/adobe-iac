import boto3
from os.path import join
import uuid



def lambda_handler(event, context):
    emr = boto3.client('emr')
    version = 'latest'
    main_path = join('s3://adobe-code-artifacts', version, 'main.py')
    modules_path = join('s3://adobe-code-artifacts', version, 'src.zip')

    job_parameters = {
        'job_name': 'job_transform',
        'input_path': 's3://logs-adobe-inbound/adobe-data.tsv',
        'output_path': 's3://logs-adobe-outbound/data1',
        'spark_config': {
            '--executor-memory': '1G',
            '--driver-memory': '2G'
        }
    }

    step_args = [
        "/usr/bin/spark-submit",
        '--py-files', modules_path,
        main_path, str(job_parameters)
    ]

    rand_str = str(uuid.uuid1())
    emr_job_name = job_parameters['job_name'] + rand_str
    step = {
        "Name": emr_job_name,
        'ActionOnFailure': 'CONTINUE',
        'HadoopJarStep': {
            'Jar': 's3://us-east-1.elasticmapreduce/libs/script-runner/script-runner.jar',
            'Args': step_args
        }
    }

    action = emr.add_job_flow_steps(JobFlowId='j-1OY5F29CYM6O0', Steps=[step])
    return action