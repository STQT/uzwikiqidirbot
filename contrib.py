import asyncio
import pprint
from asyncio import Task
from typing import Any

import aiohttp
from dotenv import load_dotenv

load_dotenv()


async def async_response(session: aiohttp.ClientSession, url: str, params: dict):
    async with session.get(url, params=params) as resp:
        pokemon = await resp.json()
        return pokemon


class WikiApi:
    URL = "https://uz.wikipedia.org/w/api.php"
    last_pages_limit = "10"
    S = aiohttp.ClientSession

    async def search_by_query(self, query: str) -> list:
        if query is None:
            return ["Topilmadi"]
        N_PAGES_PARAMS = {
            "srprop": "",
            "srenablerewrites": "true",
            "srsearch": query,
            "list": "search",
            "action": "query",
            "uselang": "uz",
            "format": "json",
        }
        async with self.S() as session:
            DATA = await async_response(session, self.URL, params=N_PAGES_PARAMS)
            search_list = DATA.get("query").get('search')

            titles_by_query = [obj.get('title') for obj in search_list]
            return titles_by_query
