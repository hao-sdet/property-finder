import json
import sys
import dataclasses
import logging
from src.utils.constants import STATES as states
from src.marketplaces import MarketPlace
from src.marketplaces import Zillow, Trulia, Redfin


class Realtor:

    def __init__(self, marketplace: MarketPlace):
        self._budget = None
        self._marketplace = marketplace

    @property
    def budget(self):
        return self._budget
    
    @budget.setter
    def budget(self, value: int):
        self._budget = value

    def get_property_details(self, address: str, city: str, state: str, zipcode: int):
        raise NotImplementedError

    def get_properties(self, city: str, state: str, limit: int = 10):
        if state not in states:
            print(f'State [{state}] does not exist!')
            return

        if limit > 100:
            print(
                'The search limit has been reached, this search will take a little longer.'
            )
        
        try:
            print(f'Looking for homes in {city}, {state} ...')
            properties = self._marketplace.search_properties(city, state, limit)
        except Exception:
            print(f'No properties found in {city}, {state}.')
        else:
            return properties

    def get_top_best_properties(self, city: str, state: str, limit: int = 10):
        raise NotImplementedError
    
    def get_top_cheapest_properties(self, city: str, state: str, limit: int = 10):
        raise NotImplementedError
    

if __name__ == '__main__':
    
    city = 'Seattle'
    state = 'WA'
    bedrooms = 3
    bathrooms = 2
    size = 1500

    marketplace = Zillow()

    realtor = Realtor(marketplace)
    realtor.budget = 1000000

    properties = realtor.get_properties(city, state, limit=100)

    # Lets shop!
    matching_properties = []
    for prop in properties:
        if (prop.bedrooms == bedrooms and prop.bathrooms == bathrooms and prop.size > size):
            matching_properties.append(prop)

    if matching_properties:
        price_sorted_properties = sorted(matching_properties, key=lambda p: p.price, reverse=False)
    else:
        sys.exit('No matching properties found!')

    cheapest_property = price_sorted_properties[0]
    print(f'Out of {len(properties)} properties, we found {cheapest_property}.')
