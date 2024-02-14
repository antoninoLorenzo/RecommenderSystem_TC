"""
asd
"""

import sys
import os
os.environ['LOKY_MAX_CPU_COUNT'] = '4'

try:
    import uvicorn
    from fastapi import FastAPI, Request
    from fastapi.middleware.cors import CORSMiddleware
except ImportError as import_err:
    print(f'[!] ImportError: {import_err}')
    sys.exit(1)

from src.data.entity import *
from src.logic.engine import UpdateEngine, RecommenderEngine, stub_offer, stub_developer


class SearchAPI:
    """
    Creates the endpoints for the Search API
    """

    def __init__(self, *args, **kwargs):
        self.__app: FastAPI = FastAPI(*args, **kwargs)
        origins = ["*"]
        self.__app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        self.__setup_called = False

    def setup(self):
        """
        Creates the endpoints to expose to the client.
        """
        self.__setup_called = True

        @self.__app.post('/engine/v1/offers/search')
        async def search_offers(request: Request):
            content = await request.json()
            developer = Developer.from_dict(content['developer'])
            return RecommenderEngine.search_offer(content['query'], developer)

        @self.__app.post('/engine/v1/offers/recommend')
        async def recommend_offers(request: Request):
            content = await request.json()
            developer = Developer.from_dict(content)
            return RecommenderEngine.recommend_offer(developer)

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
    uvicorn.run(api.app, port=8000, host='0.0.0.0')


if __name__ == "__main__":
    launch()
