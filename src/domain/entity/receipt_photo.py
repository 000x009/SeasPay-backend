from src.domain.value_objects.receipt_photo import PhotoID, Photo, Filename


class ReceiptPhoto:
    __slots__ = (
        'photo_id',
        'photo',
        'filename',
    )

    def __init__(
        self,
        photo_id: PhotoID,
        photo: Photo,
        filename: Filename,
    ):
        self.photo_id = photo_id
        self.photo = photo
        self.filename = filename

    def __str__(self):
        return f'ReceiptPhoto(photo_id={self.photo_id})'

    def __repr__(self):
        return self.__str__()
    