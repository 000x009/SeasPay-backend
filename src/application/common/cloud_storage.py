from typing import Protocol
from abc import abstractmethod

from src.domain.entity.yandex_cloud import StorageObject, PresignedPost
from src.domain.value_objects.yandex_cloud import Bucket, ObjectKey


class CloudStorage(Protocol):
    @abstractmethod
    def upload_object(self, storage_object: StorageObject) -> StorageObject:
        raise NotImplementedError
    
    @abstractmethod
    def get_object_file(self, bucket: Bucket, name: ObjectKey) -> StorageObject:
        raise NotImplementedError

    @abstractmethod
    def generate_presigned_post(self, bucket: Bucket, name: ObjectKey) -> PresignedPost:
        raise NotImplementedError
