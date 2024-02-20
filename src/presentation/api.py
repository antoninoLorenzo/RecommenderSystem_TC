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
            print(content)
            developer = Developer.from_dict(content[1])
            if content[0] == 'RECOMMEND':
                return RecommenderEngine.recommend_offer(developer)
            return RecommenderEngine.search_offer(content[0], developer)

        @self.__app.post('/engine/v1/offers/recommend')
        async def recommend_offers(request: Request):
            content = await request.json()
            developer = Developer.from_dict(content[1])
            return RecommenderEngine.recommend_offer(developer)

        @self.__app.post('/engine/v1/developers')
        async def recommend_developers(request: Request):
            content = await request.json()
            print(content)
            offer = Offer.from_dict(content)

            output = RecommenderEngine.recommend_developer(offer)
            _output = []
            for o in output:
                out = o.to_dict()
                _id = out['_Developer__id'].tolist()[0]
                out['_Developer__id'] = _id

                _languages = []
                for l in out['_Developer__languages']:
                    _lang_id = l['_Language__id'].tolist()[0]
                    _lang_code = l['_Language__code']
                    _language = Language(_lang_id, _lang_code)
                    _languages.append(_language)
                out['_Developer__languages'] = _languages

                _output.append(out)
            return _output

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
