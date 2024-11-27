from src.application.common.cloud_storage import CloudStorage
from src.application.dto.cloud import (
    GetPresignedPostDTO,
    PresignedPostDTO,
    UploadObjectDTO,
    UploadedObjectResultDTO,
    GetObjectDTO,
    ObjectDTO,
)
from src.domain.value_objects.yandex_cloud import Bucket, ObjectKey, File
from src.domain.entity.yandex_cloud import StorageObject, PresignedObject
from src.infrastructure.config import app_settings
from src.domain.value_objects.yandex_cloud import ObjectURL


class CloudService:
    def __init__(self, storage_client: CloudStorage) -> None:
        self.storage_client = storage_client

    def get_object_presigned_post(self, data: GetPresignedPostDTO) -> PresignedPostDTO:
        presigned_post = self.storage_client.generate_presigned_post(
            bucket=Bucket(app_settings.cloud_settings.receipts_bucket_name),
            name=ObjectKey(data.filename),
        )
        presigned_object = PresignedObject(
            bucket=Bucket(app_settings.cloud_settings.receipts_bucket_name),
            key=ObjectKey(data.filename),
        )

        return PresignedPostDTO(
            url=presigned_post.presigned_url.value,
            object_url=presigned_object.get_object_url(app_settings.cloud_settings.base_storage_url).value,
            data=presigned_post.data.value,
        )

    def upload_object(self, data: UploadObjectDTO) -> UploadedObjectResultDTO:
        storage_object = self.storage_client.upload_object(StorageObject(
            bucket=Bucket(data.bucket),
            key=ObjectKey(data.filename),
            file=File(data.file),
        ))
        url = storage_object.get_object_url(app_settings.cloud_settings.base_storage_url).value

        return UploadedObjectResultDTO(url=url)

    def get_object(self, data: GetObjectDTO) -> StorageObject:
        object_url = ObjectURL(data.url)
        storage_object = self.storage_client.get_object_file(
            bucket=Bucket(object_url.get_bucket()),
            name=ObjectKey(object_url.get_key()),
        )

        return ObjectDTO(
            file=storage_object.file.value,
            key=storage_object.key.value,
            bucket=storage_object.bucket.value,
        )
