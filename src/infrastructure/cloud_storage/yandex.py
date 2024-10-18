from src.application.common.cloud_storage import CloudStorage
from src.domain.entity.yandex_cloud import (
    StorageObject,
    PresignedPost,
)
from src.domain.value_objects.yandex_cloud import (
    Bucket,
    ObjectKey,
    File,
    PresignedURL,
    PresignedPostPolicy,
    PresignedPostSignature,
    AccessKeyId,
)


EXPIRES_IN = 10


class YandexCloudStorage(CloudStorage):
    def __init__(self, client) -> None:
        self.client = client

    def upload_object(self, storage_object: StorageObject) -> StorageObject:
        self.client.upload_fileobj(
            storage_object.file.value,
            storage_object.bucket.value,
            storage_object.name.value,
        )

        return storage_object

    def get_object_file(self, bucket: Bucket, name: ObjectKey) -> StorageObject:
        response = self.client.get_object(Bucket=bucket.value, Key=name.value)
        file_ = response['Body'].read()

        return StorageObject(
            name=name,
            bucket=bucket,
            file=File(file_)
        )

    def generate_presigned_post(self, bucket: Bucket, name: ObjectKey) -> PresignedPost:
        response = self.client.generate_presigned_post(
            Bucket=bucket.value,
            Key=name.value,
            ExpiresIn=EXPIRES_IN,
        )

        return PresignedPost(
            presigned_url=PresignedURL(response['url']),
            key=ObjectKey(response['fields']['key']),
            access_key_id=AccessKeyId(response['fields']['AWSAccessKeyId']),
            signature=PresignedPostSignature(response['fields']['signature']),
            policy=PresignedPostPolicy(response['fields']['policy']),
        )
