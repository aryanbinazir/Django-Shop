import boto3
from django.conf import settings

class Bucket:
    """CDN bucket manager

    init method creates connection.
    """
    def __init__(self):
        self.conn = boto3.client(
            service_name=settings.AWS_SERVICE_NAME,
            endpoint_url=settings.AWS_S3_ENDPOINT_URL,
            aws_access_key_id=settings.AWS_S3_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
         )

    def get_objects(self):
        result = self.conn.list_objects_v2(Bucket=settings.AWS_STORAGE_BUCKET_NAME)
        if result['KeyCount']:
            return result['Contents']
        return None

    def delete_object(self, key):
        self.conn.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=key)
        return True

    def download_object(self, key):
        with open(f'download({key})', 'wb') as f:
            self.conn.download_fileobj(settings.AWS_STORAGE_BUCKET_NAME, key, f)
        return True

bucket = Bucket()