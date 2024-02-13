"""
The following tests will cover OfferModel and DeveloperModel.
The following methods of OfferModel and DeveloperModel in model.py are tested:

- **similar_items**
- **add_item**
- **update_item**
- **remove_item**

## OfferCluster
_similar_items(developer: Developer) -> list[Offer]
_add_offer(offer: Offer)
_update_offer(offer: Offer)
_remove_offer(offer: Offer)

## DeveloperCluster


"""
import unittest
import tracemalloc

from src.data.entity import *
from src.logic.model import *
from src.logic.engine import stub_offer, stub_developer
from test import performance_test, display_top


OFFER_MODEL = ModelManager.get_offers_model()


class ModelTest(unittest.TestCase):
    """
    Implementation of model.py tests
    """

    def test_operations(self):
        def test_performance():
            recommendation = OFFER_MODEL.similar_items(stub_developer)
            print(f'Recommended Offers: \n{recommendation}')

            OFFER_MODEL.add_item(stub_offer)
            test_add = OFFER_MODEL.get_item(1000)
            print(f'Test Add: \n{test_add}')

            new_skills = [
                Skill(1001, "TensorFlow", "Framework_2"),
                Skill(1002, "Pandas", "Framework_2"),
                Skill(1003, "PyTorch", "Framework_2"),
                stub_offer.skills.pop(0)
            ]
            stub_offer.skills = new_skills

            OFFER_MODEL.update_item(stub_offer)
            test_update = OFFER_MODEL.get_item(1000)
            print(f'Test Update: \n{test_update}')

            OFFER_MODEL.remove_item(stub_offer)
            test_remove = OFFER_MODEL.get_item(1000)
            print(f'Test Remove: \n{test_remove}')

        tracemalloc.start()
        test_performance()
        snapshot = tracemalloc.take_snapshot()
        display_top(snapshot, limit=5)


if __name__ == "__main__":
    unittest.main()
