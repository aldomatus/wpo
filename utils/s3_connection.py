# Python
import pytz
import uuid
from datetime import datetime

# Boto3
import boto3


def save_document(base64_pdf, category, uuid_sport_location):
    # GET current date from time zone
    time_zone = pytz.timezone("America/Mexico_City")
    current_date = datetime.today().astimezone(time_zone)

    response_url = save_file(base64_pdf, category, "mx", uuid_sport_location)
    return response_url


def save_file(file_bytes_io, category, country_code, uuid_sport_location):
    bucket_name = "weplayone-development-startup"
    s3_region = "s3.amazonaws.com"
    s3 = boto3.resource("s3")
    name_uuid = str(uuid.uuid4())
    name_file = f"{country_code}/{category}/{uuid_sport_location}/{name_uuid}.jpg"
    object_to = s3.Object(bucket_name, name_file)
    object_to.put(
        Body=file_bytes_io, ACL="public-read"
    )
    url_response_to_send = f"https://{bucket_name}.{s3_region}/{name_file}"
    return url_response_to_send
