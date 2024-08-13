from enum import StrEnum

from pydantic import BaseModel


# https://github.com/qbittorrent/qBittorrent/wiki/Web-API-Documentation/87ec6b289ea5376b648e8cbb1373fb538da9f01d#authentication
class LoginRequest(BaseModel):
    username: str
    password: str


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
