from src.application.common.cloud_storage import CloudStorage
from src.domain.entity.yandex_cloud import StorageObject
from src.domain.value_objects.yandex_cloud import Bucket, ObjectName, File


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

    def get_object_file(self, bucket: Bucket, name: ObjectName) -> StorageObject:
        response = self.client.get_object(Bucket=bucket.value, Key=name.value)
        file_ = response['Body'].read()

        return StorageObject(
            name=name,
            bucket=bucket,
            file=File(file_)
        )
