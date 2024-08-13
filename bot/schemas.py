from enum import StrEnum
from typing import Annotated

from pydantic import (
    BaseModel,
    Field,
    FieldSerializationInfo,
    RootModel,
    field_serializer,
)


# https://github.com/qbittorrent/qBittorrent/wiki/Web-API-Documentation/87ec6b289ea5376b648e8cbb1373fb538da9f01d#authentication
class LoginRequest(BaseModel):
    username: str
    password: str


# https://github.com/qbittorrent/qBittorrent/wiki/Web-API-Documentation/87ec6b289ea5376b648e8cbb1373fb538da9f01d#add-new-torrent
class AddTorrentRequest(BaseModel):
    urls: list[str]
    savepath: str | None = None
    category: str | None = None
    skip_checking: bool | None = None
    paused: bool | None = None
    root_folder: bool | None = None
    rename: str | None = None

    up_limit: Annotated[
        str | None,
        Field(serialization_alias="upLimit"),
    ] = None

    dl_limit: Annotated[
        str | None,
        Field(serialization_alias="dlLimit"),
    ] = None

    auto_tmm: Annotated[
        bool | None,
        Field(serialization_alias="autoTMM"),
    ] = None

    sequential_download: Annotated[
        bool | None,
        Field(serialization_alias="sequentialDownload"),
    ] = None

    @field_serializer("urls")
    def serialize_urls(self, urls: list[str], _info: FieldSerializationInfo):
        return "\n".join(urls)


class TorrentState(StrEnum):
    ERROR = "error"
    MISSING_FILES = "missingFiles"
    UPLOADING = "uploading"
    PAUSED_UP = "pausedUP"
    QUEUED_UP = "queuedUP"
    STALLED_UP = "stalledUP"
    CHECKING_UP = "checkingUP"
    FORCED_UP = "forcedUP"
    ALLOCATING = "allocating"
    DOWNLOADING = "downloading"
    META_DL = "metaDL"
    PAUSED_DL = "pausedDL"
    QUEUED_DL = "queuedDL"
    STALLED_DL = "stalledDL"
    CHECKING_DL = "checkingDL"
    FORCE_DL = "forceDL"
    CHECKING_RESUME_DATA = "checkingResumeData"
    MOVING = "moving"
    UNKNOWN = "unknown"


# https://github.com/qbittorrent/qBittorrent/wiki/Web-API-Documentation/87ec6b289ea5376b648e8cbb1373fb538da9f01d#get-torrent-list
class TorrentListResponse(BaseModel):
    name: str
    eta: int
    hash: str
    amount_left: int
    category: str
    downloaded: int
    dlspeed: int
    uploaded: int
    upspeed: int
    magnet_uri: str
    max_ratio: float
    progress: float
    ratio: float
    size: int
    state: TorrentState
    tags: str
    total_size: int


class CategoryInfo(BaseModel):
    name: str
    save_path: Annotated[str, Field(alias="savePath")]


CategoryInfoResponse = RootModel[dict[str, CategoryInfo]]


class AddCategoryRequest(BaseModel):
    name: Annotated[str, Field(serialization_alias="category")]
    save_path: Annotated[
        str,
        Field(serialization_alias="savePath"),
    ] | None = None


class RemoveCategoriesRequest(BaseModel):
    categories: list[str]

    @field_serializer("categories")
    def serialize_categories(
            self,
            categories: list[str],
            _info: FieldSerializationInfo,
    ):
        return "\n".join(categories)
