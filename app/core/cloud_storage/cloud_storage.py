from abc import ABC
from abc import abstractmethod
from typing import Any

import boto3
import cloudinary
from cloudinary import uploader
from google.cloud import storage


class CloudStorage(ABC):
    @abstractmethod
    def upload_file(self, file_content: bytes, filename: str) -> Any:
        pass

    @abstractmethod
    def delete_file(self, identifier: str) -> None:
        pass


# GCS ( Google Cloud Storage)
class GoogleCloudStorage(CloudStorage):
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.client = storage.Client()

    def upload_file(self, file_content: bytes, filename: str) -> str:
        bucket = self.client.get_bucket(self.bucket_name)
        blob = bucket.blob(filename)
        blob.upload_from_string(file_content)
        return blob.public_url

    def delete_file(self, filename: str) -> None:
        blob = self.client.get_bucket(self.bucket_name).blob(filename)
        blob.delete()


# Amazon S3
class AmazonS3Storage(CloudStorage):
    def __init__(
        self, bucket_name, aws_access_key_id, aws_secret_access_key, region_name
    ):
        self.bucket_name = bucket_name
        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name,
        )

    def upload_file(self, file_content: bytes, filename: str) -> str:
        self.s3.upload_fileobj(file_content, self.bucket_name, filename)
        file_url = f"https://{self.bucket_name}.s3.amazonaws.com/{filename}"
        return file_url

    def delete_file(self, filename: str) -> None:
        self.s3.delete_object(Bucket=self.bucket_name, Key=filename)


# Cloudinary
class CloudinaryStorage(CloudStorage):
    def __init__(self, cloud_name, api_key, api_secret):
        cloudinary.config(cloud_name=cloud_name, api_key=api_key, api_secret=api_secret)

    def upload_file(self, file_content: bytes, filename: str) -> Any:
        result = uploader.upload(
            file_content,
            folder="test",
            resource_type="raw",
            filename=filename,
            use_filename=True,
        )
        return result

    def delete_file(self, public_id: str) -> None:
        uploader.destroy(public_id=public_id, resource_type="raw")
