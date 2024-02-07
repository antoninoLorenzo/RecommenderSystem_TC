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

from src.data.entity import Developer, Offer, Location, Skill, Language, Employer


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
            # print(Developer.from_dict(content['user']))
            print('Developer: ')
            pprint(content)

            return [
                Offer(1, 'Web Developer', 'active', 'desc',
                      Employer(1, "Antonino", "Lorenzo", "anton@gmail.com", "1234", "asd"),
                      'Remote',
                      Location(1, "Avellino Italia", 123, 124),
                      [Skill(1, "Python", "Programming Language")],
                      [Language(1, "it")]),
                Offer(2, 'Frontend Developer', 'active', 'desc',
                      Employer(1, "Antonino", "Lorenzo", "anton@gmail.com", "1234", "asd"),
                      'Remote',
                      Location(1, "Avellino Italia", 123, 124),
                      [Skill(1, "Python", "Programming Language")],
                      [Language(1, "it")]),
            ]

        @self.__app.post('/engine/v1/developers/search')
        def search_developers(query: str):
            return {'query': query}

        @self.__app.post('/engine/v1/developers/recommend')
        async def recommend_developers(request: Request):
            pass

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
