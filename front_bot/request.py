import os
from typing import List, Optional, Tuple, Dict

import aiohttp

url = os.getenv('BASE_URL')


class Fetcher:
    base_url = url
    _session: Optional[aiohttp.ClientSession] = None
    auth: Optional[Tuple[str, str]] = None
    timeout: Optional[int] = None
    headers: Optional[Dict] = None

    @property
    def session(self):
        if not self._session or self._session.closed:
            auth = aiohttp.BasicAuth(*self.auth) if self.auth else None
            timeout = aiohttp.ClientTimeout(total=self.timeout)
            trace_config = aiohttp.TraceConfig()

            self._session = aiohttp.ClientSession(
                auth=auth, headers=self.headers,
                timeout=timeout, trace_configs=[trace_config]
            )

        return self._session

    async def get(self, endpoint: str, file: bool = False):
        async with self.session as async_session:
            async with async_session.request(
                    'GET', self.base_url + endpoint, verify_ssl=False
            ) as response:
                if file:
                    return await response.content.read()
                return await response.json()

    async def post(self, endpoint: str, payload: dict):
        async with self.session as async_session:
            async with async_session.request(
                'POST', self.base_url + endpoint, verify_ssl=False, **payload
            ) as response:
                return await response.json()



