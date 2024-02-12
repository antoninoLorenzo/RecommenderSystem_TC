from src.data import Item
from src.data.entity import Offer, Developer, Skill, Location, Language, Employer
from src.service.model import OfferModel

stub_offer = Offer(1, 'Web Developer', 'active', 'desc',
                   Employer(1, "Antonino", "Lorenzo", "anton@gmail.com", "DioCiao0003", "asd"),
                   'Remote',
                   Location(1, "Avellino Italia", 123, 124),
                   [Skill(1, "Python", "Programming Language")],
                   [Language(1, "it")])

stub_developer = Developer(1, 'Antonino', 'Lorenzo', 'bio',
                           'anton@asd.com', 'DioCiao0003', [Language(1, 'it')],
                           Location(1, 'Avellino', 83.0, 100.0),
                           [Skill(1, 'Java', 'Programming Language')]
                           )
OFFER_MODEL = OfferModel()

class RecommenderEngine:

    def search_offer(self, query: str, user: Developer):
        # find offer from search given query and find similar offers using developer skills
        # the result will be an ordered list with  the similar offers that were also found by search,
        # then the offers found by query but not by similarity
        return OFFER_MODEL.similar_items(user)

    def recommend_developer(self, offer: Offer):
        return DeveloperModelStub().similar_items(offer)


class UpdateEngine:

    def add(self, item: Item):
        if isinstance(item, Offer):
            OFFER_MODEL.add_item(item)
        elif isinstance(item, Developer):
            DeveloperModelStub().add_item(item)
        else:
            raise ValueError(f'Invalid parameter Item: {item}')

    def update(self, item: Item):
        if isinstance(item, Offer):
            OFFER_MODEL.update_item(item)
        elif isinstance(item, Developer):
            DeveloperModelStub().update_item(item)
        else:
            raise ValueError(f'Invalid parameter Item: {item}')

    def remove(self, item: Item):
        if isinstance(item, Offer):
            OFFER_MODEL.remove_item(item)
        elif isinstance(item, Developer):
            DeveloperModelStub().remove_item(item)
        else:
            raise ValueError(f'Invalid parameter Item: {item}')


class DeveloperModelStub:
    """
    Interface for OfferModel and Developer Model.
    """

    def similar_items(self, item: Item) -> list[Item]:
        """
        :param item: Item Type A
        :return: list[Item Type B]
        """
        if not isinstance(item, Offer):
            raise ValueError("Not an offer")

        return [stub_developer, stub_developer]

    def add_item(self, item: Item):
        """
        :param item: should be the same type of model items and shouldn't be present in model
        """
        if not isinstance(item, Developer):
            raise ValueError("Not a developer")

    def update_item(self, item: Item):
        """
        :param item: should be the same type of model items and item should be present in model
        """
        if not isinstance(item, Developer):
            raise ValueError("Not a developer")

    def remove_item(self, item: Item):
        """
        :param item: should be the same type of model items and item should be present in model
        """
        if not isinstance(item, Developer):
            raise ValueError("Not a developer")
