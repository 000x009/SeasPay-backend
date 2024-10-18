from src.application.common.cloud_storage import CloudStorage
from src.application.dto.cloud import GetPresignedURL, PresignedURL


class CloudService:
    def __init__(self, storage_client: CloudStorage) -> None:
        self.storage_client = storage_client

    def get_object_presigned_url(self, data: GetPresignedURL) -> PresignedURL:

