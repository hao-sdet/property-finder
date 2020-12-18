import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
from .base import MarketPlace
from src.common.exceptions import PageNotFoundError
from src.models import Property


class Zillow(MarketPlace):
    
    def __init__(self):
        self.zillow_base_url = 'https://www.zillow.com'
        self.zillow_home_sale_url = f'{self.zillow_base_url}/homes/for_sale'
        self.request_headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.8',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
        }
        self.maximun_pages = 10

    def _get_property_details(self, listing):
        try:
            address = listing.find('address', {'class': 'list-card-addr'}).get_text()
            price = listing.find('div', {'class': 'list-card-price'})
            price = int(price.get_text().replace(',','').replace('$',''))
            bedroom, bathroom, size = listing.find_all('li', {'class': ''})
            bedrooms = int(bedroom.get_text().split(' ')[0])
            bathrooms = int(bathroom.get_text().split(' ')[0])
            size = int(size.get_text().split(' ')[0].replace(',',''))
        except:
            return None
        else:
            return Property(address, price, bedrooms, bathrooms, size)

    def _get_properties(self, web_content):
        properties = []
        soup = BeautifulSoup(web_content, 'lxml')
        listings = soup.find_all('div', {'class': 'list-card-info'})
        for listing in listings:
            p = self._get_property_details(listing)
            if p:
                properties.append(p)

        return properties

    def requests(self, url: str, headers: dict):
        try:
            with requests.Session() as s:
                resp = s.get(url, headers=headers)
        except Exception as error:
            raise error
        else:
            if resp.status_code == 200:
                return resp

    def search_properties(self, city: str, state: str, limit: int = 10):
        results = []
        for page in range(1, self.maximun_pages + 1):
            url = f'{self.zillow_home_sale_url}/{city}-{state}/{page}_p/'
            resp = self.requests(url, self.request_headers)
            if not resp:
                raise PageNotFoundError(f'This {url} cant be found!')
            
            properties = self._get_properties(resp.content)
            if properties:
                results.extend(properties)
            else:
                return results

            if len(results) > limit:
                return results[:limit]

        return results

    def search_properties_by_price(self, city: str, state: str, min_price: int, max_price: int, limit: int = 10):
        properties = []
        found_properties = self.search_properties(city, state, limit)
        for fp in found_properties:
            if fp.price > min_price and fp.price < max_price:
                properties.append(fp)
        
        return properties
    
    def search_properties_by_address(self, address: str, city: str, state: str, zipcode: int):
        found_properties = self.search_properties(city, state, limit=100)
        for fp in found_properties:
            if address.lower() in fp.address.lower():
                return fp
        else:
            raise PropertyNotFoundError(f'Could not find [{address}] property!')
