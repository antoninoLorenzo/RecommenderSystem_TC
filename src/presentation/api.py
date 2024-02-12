"""
asd
"""

import sys
from pprint import pprint

try:
    import uvicorn
    from fastapi import FastAPI, Request
except ImportError as import_err:
    print(f'[!] ImportError: {import_err}')
    sys.exit(1)

from src.presentation import UpdateEngine, RecommenderEngine, stub_offer, stub_developer
from src.data.entity import *


class SearchAPI:
    """
    Creates the endpoints for the Search API
    """

    def __init__(self, *args, **kwargs):
        self.__app: FastAPI = FastAPI(*args, **kwargs)
        self.__setup_called = False

    def setup(self):
        """
        Creates the endpoints to expose to the client.
        """
        self.__setup_called = True

        @self.__app.post('/engine/v1/offers')
        async def search_offers(request: Request):
            content = await request.json()
            developer = Developer.from_dict(content[1])
            return RecommenderEngine.search_offer(content[0], developer)

        @self.__app.post('/engine/v1/developers')
        async def recommend_developers(request: Request):
            RecommenderEngine.recommend_developer(stub_offer)
            return [stub_developer, stub_developer]

        @self.__app.post('/engine/v1/add')
        async def add(request: Request):
            UpdateEngine().add(
                await request.json()
            )

        @self.__app.post('/engine/v1/update')
        async def add(request: Request):
            UpdateEngine().update(
                await request.json()
            )

        @self.__app.post('/engine/v1/remove')
        async def add(request: Request):
            UpdateEngine().remove(
                await request.json()
            )

    @property
    def app(self):
        """
        FastAPI app.
        """
        if self.__setup_called:
            return self.__app
        raise RuntimeError('[!] Must initialize API')


def launch():
    """

    """
    api = SearchAPI()
    api.setup()
    uvicorn.run(api.app, port=8000, host='127.0.0.1')


if __name__ == "__main__":
    launch()
