
class MarketPlace:

    def search_properties(self, city: str, state: str, limit: int = 10):
        raise NotImplementedError

    def search_properties_by_price(self, city: str, state: str, min_price: int, max_price: int, limit: int = 10):
        raise NotImplementedError
    
    def search_properties_by_address(self, address: str, city: str, state: str, zipcode: int):
        raise NotImplementedError
