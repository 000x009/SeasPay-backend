import uuid
from typing import Optional

from src.domain.value_objects.yandex_cloud import (
    ObjectKey,
    Bucket,
    File,
    ObjectURL,
    PresignedURL,
    AccessKeyId,
    PresignedPostSignature,
    PresignedPostPolicy,
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
        return ObjectURL(f'{base_storage_url}/{self.bucket.value}/{self.name.value}')

    def _generate_object_name(self) -> ObjectKey:
        return ObjectKey(uuid.uuid4().hex)



class PresignedPost:
    __slots__ = (
        'presigned_url',
        'key',
        'access_key_id',
        'signature',
        'policy',

    )

    def __init__(
        self,
        presigned_url: PresignedURL,
        key: ObjectKey,
        access_key_id: AccessKeyId,
        signature: PresignedPostSignature,
        policy: PresignedPostPolicy,
    ) -> None:
        self.presigned_url = presigned_url
        self.key = key
        self.access_key_id = access_key_id
        self.signature = signature
        self.policy = policy

