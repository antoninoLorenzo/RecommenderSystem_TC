











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
