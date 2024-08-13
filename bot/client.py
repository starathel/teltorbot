from aiohttp import ClientSession, CookieJar
from pydantic import TypeAdapter
from yarl import URL

from bot.errors import (
    AuthorizationFailedException,
    EmptyCategoryNameError,
    InvalidCategoryNameError,
    UnknownError,
)
from bot.schemas import (
    AddCategoryRequest,
    AddTorrentRequest,
    CategoryInfo,
    CategoryInfoResponse,
    LoginRequest,
    RemoveCategoriesRequest,
    TorrentListResponse,
)
from bot.settings import get_settings


class QbitWebClient:
    def __init__(self, session: ClientSession | None = None) -> None:
        settings = get_settings()
        if session is None:
            session = ClientSession(
                cookie_jar=CookieJar(unsafe=settings.qbitweb.unsafe_cookies),
            )
        self.session = session

        self.base_url = URL(str(settings.qbitweb.url))

    async def close(self) -> None:
        await self.session.close()

    async def authorize(self) -> None:
        settings = get_settings()
        login_data = LoginRequest(
            username=settings.qbitweb.username,
            password=settings.qbitweb.password,
        )
        async with self.session.post(
            self.base_url / "auth" / "login",
            data=login_data.model_dump(),
        ) as resp:
            if resp.status != 200 or not resp.cookies:
                raise AuthorizationFailedException

    async def torrents_list(self) -> list[TorrentListResponse] | None:
        url = self.base_url / "torrents" / "info"
        async with self.session.get(url) as resp:
            if resp.status != 200:
                return None
            ta = TypeAdapter(list[TorrentListResponse])
            return ta.validate_json(await resp.text())

    async def add_torrent(
            self,
            magnet: str,
            category: str | None = None,
            rename: str | None = None,
            override_path: str | None = None,
            sequential_download: bool = False,
    ) -> None:
        request_data = AddTorrentRequest(
            urls=[magnet],
            category=category,
            rename=rename,
            savepath=override_path,
            sequential_download=sequential_download,

            root_folder=True,
            auto_tmm=True,
        ).model_dump(exclude_none=True, by_alias=True)
        url = self.base_url / "torrents" / "add"

        async with self.session.post(url, data=request_data) as resp:
            if resp.status != 200:
                raise UnknownError

    async def categories_list(self) -> list[CategoryInfo]:
        url = self.base_url / "torrents" / "categories"

        async with self.session.get(url) as resp:
            if resp.status != 200:
                raise UnknownError

            categories_response = CategoryInfoResponse.model_validate_json(
                await resp.text()
            )
        return list(categories_response.root.values())

    async def add_category(
            self,
            name: str,
            save_path: str | None = None,
    ) -> None:
        url = self.base_url / "torrents" / "createCategory"
        request_data = AddCategoryRequest(
            name=name,
            save_path=save_path,
        ).model_dump(exclude_none=True, by_alias=True)

        async with self.session.post(url, data=request_data) as resp:
            if resp.status == 400:
                raise EmptyCategoryNameError
            if resp.status == 409:
                raise InvalidCategoryNameError
            if resp.status != 200:
                raise UnknownError

    async def remove_categories(self, categories: list[str]) -> None:
        url = self.base_url / "torrents" / "removeCategories"
        request_data = RemoveCategoriesRequest(
            categories=categories,
        ).model_dump(by_alias=True)

        async with self.session.post(url, data=request_data) as resp:
            if resp.status != 200:
                raise UnknownError
