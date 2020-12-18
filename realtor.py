import json
import sys
import dataclasses
import logging
from src.marketplaces import MarketPlace
from src.marketplaces import Zillow, Trulia, Redfin
from src.utils.constants import STATES as states
from src.utils.prompter import Prompter


class Realtor:

    def __init__(self, marketplace: MarketPlace):
        self._marketplace = marketplace

    def get_property_details(self, address: str, city: str, state: str, zipcode: int):
        raise NotImplementedError

    def get_properties(self, city: str, state: str, limit: int = 10):
        if state.upper() not in states:
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


if __name__ == '__main__':
    
    p = Prompter(welcome_message='Home Finder')
    city        =  p.prompt('Name of the city: ', answer_length=20)
    state       = p.prompt('Name of the state: ', answer_length=2)
    bedrooms    = p.prompt('Number of bedrooms: ', answer_type=int)
    bathrooms   = p.prompt('Number of bathrooms: ', answer_type=int)
    size        = p.prompt('Lot size (sqft): ', answer_type=int)

    marketplace = Zillow()
    realtor = Realtor(marketplace)

    # Found properties
    properties = realtor.get_properties(city, state, limit=100)

    # Get 10 lowest price properties
    matching_properties = []
    for prop in properties:
        if (prop.bedrooms == bedrooms and prop.bathrooms == bathrooms and prop.size > size):
            matching_properties.append(prop)

    if matching_properties:
        price_sorted_properties = sorted(matching_properties, key=lambda p: p.price, reverse=False)
    else:
        sys.exit('No matching properties found!')

    cheapest_property = price_sorted_properties[:10]
    print(f'Out of {len(properties)} properties, the top cheapeast properties are:')
    for cp in cheapest_property:
        json_formatted = json.dumps(dataclasses.asdict(cp))
        print(json_formatted)
