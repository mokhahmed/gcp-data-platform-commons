import re
from google.cloud import storage



def copy_blob(bucket_name, blob_name, destination_bucket_name, destination_blob_name):
    """Copies a blob from one bucket to another with a new name."""

    storage_client = storage.Client()

    source_bucket = storage_client.bucket(bucket_name)
    source_blob = source_bucket.blob(blob_name)
    destination_bucket = storage_client.bucket(destination_bucket_name)

    blob_copy = source_bucket.copy_blob(
        source_blob, destination_bucket, destination_blob_name
    )

    print(
        "Blob {} in bucket {} copied to blob {} in bucket {}.".format(
            source_blob.name,
            source_bucket.name,
            blob_copy.name,
            destination_bucket.name,
        )
    )


def is_valid_dag(dags_path):
    # pattern is a string containing the regex pattern
    try:
        pattern = re.compile(r"dags\/apps\/\w+\/.*py")
        if re.fullmatch(pattern, dags_path):
            return True
        else:
            return False
    except re.error:
        print("Non valid regex pattern")
        exit()


def validate_n_deploy_dags(event, context):

    print(f"New file {event['attributes']['objectId']} published....")

    source_bucket = 'tmp-dags-bkt-01'
    target_bucket = 'dags-bkt-01'

    file_name = event['attributes']['objectId']

    if is_valid_dag(file_name):
        copy_blob(source_bucket, file_name, target_bucket, file_name)
    else:
        print("dags is not valid and will not be copied to the dags bucket...")

