import os
import boto3
import tempfile
from dotenv import load_dotenv
from urllib.parse import urlparse
from botocore.exceptions import ClientError

class S3Client:

    def __init__(self):
        load_dotenv()
        self.client = boto3.client(
            's3',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_REGION', 'us-east-1')
        )

    def parse_s3_url(self, s3_url: str) -> tuple[str, str]:
        parsed = urlparse(s3_url)
        host = parsed.netloc
        path = parsed.path.lstrip('/')
        if ".s3" in host and host.endswith("amazonaws.com"):
            bucket = host.split(".")[0]
        else:
            bucket = parsed.netloc or s3_url.split("s3://")[1].split("/")[0]

        return bucket, path
    
    def download_to_tmp(self, s3_url: str) -> str:
        bucket, key = self.parse_s3_url(s3_url)
        tmp_dir = tempfile.gettempdir()
        local_path = os.path.join(tmp_dir, os.path.basename(key))
        try:
            self.client.download_file(bucket, key, local_path)
        except ClientError as e:
            code = e.response["Error"]["Code"]
            msg  = e.response["Error"]["Message"]
            raise RuntimeError(f"Erro ao baixar S3 (bucket={bucket}, key={key}): {code} – {msg}")
        return local_path

    def upload_to_s3(self, local_path: str, key: str):
        self.client.upload_file(local_path, os.getenv("BUCKET"), key)
