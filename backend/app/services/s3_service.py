import boto3

from botocore.config import Config

from app.core.config import settings


s3 = boto3.client(

    "s3",

    endpoint_url=settings.s3_endpoint_url,

    aws_access_key_id=settings.aws_access_key_id,

    aws_secret_access_key=settings.aws_secret_access_key,

    region_name=settings.aws_region,

    config=Config(
        s3={
            "addressing_style": "path"
        }
    )
)


def ensure_bucket():

    try:

        s3.head_bucket(
            Bucket=settings.s3_bucket
        )

    except Exception:

        s3.create_bucket(
            Bucket=settings.s3_bucket
        )


def upload_bytes(
    key: str,
    data: bytes,
    content_type: str
):

    ensure_bucket()

    s3.put_object(

        Bucket=settings.s3_bucket,

        Key=key,

        Body=data,

        ContentType=content_type
    )