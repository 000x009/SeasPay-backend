import uuid
from typing import Optional

from src.domain.value_objects.yandex_cloud import (
    ObjectKey,
    Bucket,
    File,
    ObjectURL,
    PresignedURL,
    PostData,
)


class StorageObject:
    """Yandex storage file object"""

    __slots__ = (
        'key',
        'bucket',
        'file',
    )

    def __init__(
        self,
        bucket: Bucket,
        file: File,
        key: Optional[ObjectKey] = None,
    ) -> None:
        self.key = key
        self.bucket = bucket
        self.file = file

        if key is None:
            self.key = self._generate_object_name()

    def get_object_url(self, base_storage_url: str) -> ObjectURL:
        return ObjectURL(f'{base_storage_url}/{self.bucket.value}/{self.key.value}')

    def _generate_object_name(self) -> ObjectKey:
        return ObjectKey(uuid.uuid4().hex)


class PresignedObject:
    """Yandex storage file object with presigned post"""

    __slots__ = (
        'key',
        'bucket',
    )

    def __init__(
        self,
        bucket: Bucket,
        key: Optional[ObjectKey] = None,
    ) -> None:
        self.key = key
        self.bucket = bucket

        if key is None:
            self.key = self._generate_object_name()

    def get_object_url(self, base_storage_url: str) -> ObjectURL:
        return ObjectURL(f'{base_storage_url}/{self.bucket.value}/{self.key.value}')


class PresignedPost:
    __slots__ = (
        'presigned_url',
        'data',
    )

    def __init__(
        self,
        presigned_url: PresignedURL,
        data: PostData,
    ) -> None:
        self.presigned_url = presigned_url
        self.data = data
