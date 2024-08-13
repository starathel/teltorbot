from aiohttp import ClientSession, CookieJar
from pydantic import TypeAdapter
from yarl import URL

from bot.errors import AuthorizationFailedException
from bot.schemas import LoginRequest, TorrentListResponse
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
