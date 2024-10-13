import uuid
from typing import Optional

from src.domain.value_objects.yandex_cloud import ObjectName, Bucket, File, ObjectURL


class StorageObject:
    """Yandex storage file object"""

    __slots__ = (
        'name',
        'bucket',
        'file',
    )

    def __init__(
        self,
        bucket: Bucket,
        file: File,
        name: Optional[ObjectName] = None,
    ) -> None:
        self.name = name
        self.bucket = bucket
        self.file = file

        if name is None:
            self.name = self._generate_object_name()

    def get_object_url(self, base_storage_url: str) -> ObjectURL:
        return ObjectURL(f'{base_storage_url}/{self.bucket}/{self.name}')

    def _generate_object_name(self) -> ObjectName:
        return ObjectName(uuid.uuid4().hex)
