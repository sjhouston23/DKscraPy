import requests
from bs4 import BeautifulSoup
from posixpath import join as urljoin


class Webpage:

    def __init__(self, event):
        dk_url = 'https://sportsbook-us-co.draftkings.com//sites/US-CO-SB/api/v4/eventgroups/'
        event_keys = {'nba': 88670846,
                      'mlb': 88670847,
                      'nfl': 88670561,
                      'cbb': 88670771}
        event_ID = event_keys[event]
        promo = 'includePromotions=true'
        form = 'format=json'
        self.url = urljoin(dk_url, str(event_ID) + '?' + promo + '&' + form)

    def soup_setup(self):
        """
        Create a BeautifulSoup object from the given url.
        Should return <Response [200]>, unless there is an error.
        """
        response = requests.get(self.url)
        print(response)
        soup = BeautifulSoup(response.text, 'html.parser')

        return soup

    def pull_data(self):
        dk_api = requests.get(self.url).json()
        markets = dk_api['eventGroup']['offerCategories'][0]['offerSubcategoryDescriptors'][0]['offerSubcategory'][
            'offers']

        return markets
