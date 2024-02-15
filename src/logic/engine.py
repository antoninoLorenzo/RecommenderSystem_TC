from src.data import Item
from src.data.entity import Offer, Developer, Skill, Employer, Language
from src.data.repository import *
from src.logic.model import OfferModel, DeveloperModel, ModelManager


stub_offer = Offer(1000, 'Web Developer', 'active', 'desc',
                   Employer(1000, "Antonino", "Lorenzo", "anton@gmail.com", "DioCiao0003", "asd"),
                   'Remote',
                   "Avellino Italia",
                   [
                       Skill(1000, "Python", "Programming Language"),
                       Skill(1001, "Pandas", "Framework")
                   ],
                   [Language(1000, "it")])

stub_developer = Developer(1000, 'Antonino', 'Lorenzo', 'bio',
                           'anton@asd.com', 'DioCiao0003', [Language(1000, 'it')],
                           'Avellino',
                           [Skill(1000, 'Java', 'Programming Language')])


OFFER_MODEL = ModelManager.get_offers_model()
DEVELOPER_MODEL = ModelManager.get_developers_model()


class RecommenderEngine:
    """
    Act as interface for business layers search operations.
    """
    @staticmethod
    def search_offer(query: str, user: Developer):
        """
        :param query: a not empty query string
        :param user: a Developer searching for an offer
        """
        if not isinstance(query, str) or not isinstance(user, Developer):
            raise ValueError('[RecommenderEngine] search_offer expects str and Developer')
        elif len(query) == 0:
            raise ValueError('[RecommenderEngine] query must not be empty')

        # Get Offers with indexing
        search_offers: list[Offer] = OfferRepository().get_offers(query)
        search_ids = [search.id for search in search_offers]

        # Get Offers with recommendation
        recommended_offers = OFFER_MODEL.similar_items(user)
        recommended_ids = [recommended.id for recommended in recommended_offers]

        # Get Common offers and remove from other lists
        intersection = set(search_ids).intersection(set(recommended_ids))
        common_offers = [offer for offer in search_offers + recommended_offers if offer.id in intersection]
        search_offers = [offer for offer in search_offers if offer.id not in intersection]
        recommended_offers = [offer for offer in recommended_offers if offer.id not in intersection]

        # Create result
        output = set(common_offers)
        while search_offers or recommended_offers:
            if search_offers:
                output.add(search_offers.pop(0))
            if recommended_offers:
                output.add(recommended_offers.pop(0))

        return output

    @staticmethod
    def recommend_offer(developer: Developer):
        return OFFER_MODEL.similar_items(developer)

    @staticmethod
    def recommend_developer(offer: Offer):
        output = DEVELOPER_MODEL.similar_items(offer)
        return set(output)



class UpdateEngine:
    """
    Act as interface for business layer update operations
    """
    def add(self, item: Item):
        if isinstance(item, Offer):
            OFFER_MODEL.add_item(item)
        elif isinstance(item, Developer):
            DEVELOPER_MODEL.add_item(item)
        else:
            raise ValueError(f'Invalid parameter Item: {item}')

    def update(self, item: Item):
        if isinstance(item, Offer):
            OFFER_MODEL.update_item(item)
        elif isinstance(item, Developer):
            DEVELOPER_MODEL.update_item(item)
        else:
            raise ValueError(f'Invalid parameter Item: {item}')

    def remove(self, item: Item):
        if isinstance(item, Offer):
            OFFER_MODEL.remove_item(item)
        elif isinstance(item, Developer):
            DEVELOPER_MODEL.remove_item(item)
        else:
            raise ValueError(f'Invalid parameter Item: {item}')