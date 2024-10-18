from src.application.common.cloud_storage import CloudStorage
from src.application.dto.cloud import GetPresignedPostDTO, PresignedPostDTO
from src.infrastructure.config import load_settings
from src.domain.value_objects.yandex_cloud import Bucket, ObjectKey


class CloudService:
    def __init__(self, storage_client: CloudStorage) -> None:
        self.storage_client = storage_client

    def get_object_presigned_post(self, data: GetPresignedPostDTO) -> PresignedPostDTO:
        settings = load_settings()
        presigned_post = self.storage_client.generate_presigned_post(
            bucket=Bucket(settings.cloud_settings.receipts_bucket_name),
            name=ObjectKey(data.filename),
        )

        return PresignedPostDTO(
            url=presigned_post.presigned_url.value,
            key=presigned_post.key.value,
            access_key_id=presigned_post.access_key_id.value,
            signature=presigned_post.signature.value,
            policy=presigned_post.policy.value,
        )
