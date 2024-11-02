from typing import Optional

from src.domain.value_objects.platform import (
    LoginData,
    WebPlace,
    ImageURL,
    PlatformID,
    Description,
    Name,
)


class Platform:
    """
    Platform, marketplace such as BeatStars, Spotify... that offers certain services/products
    """

    __slots__ = (
        'name',
        'image_url',
        'web_place',
        'description',
        'login_data',
    )

    def __init__(
        self,
        name: Name,
        image_url: ImageURL,
        web_place: Optional[WebPlace] = None,
        description: Optional[Description] = None,
        login_data: Optional[LoginData] = None,
    ) -> None:
        self.name = name
        self.image_url = image_url
        self.web_place = web_place
        self.description = description
        self.login_data = login_data


class PlatformDB(Platform):
    __slots__ = ('platform_id',)

    def __init__(
        self,
        platform_id: PlatformID,
        name: Name,
        image_url: ImageURL,
        web_place: Optional[WebPlace] = None,
        description: Optional[Description] = None,
        login_data: Optional[LoginData] = None,
    ) -> None:
        self.platform_id = platform_id
        self.web_place = web_place
        if self.web_place is None:
            self.web_place = WebPlace(self.platform_id.value)

        super().__init__(
            name=name,
            image_url=image_url,
            web_place=web_place,
            description=description,
            login_data=login_data,
        )
