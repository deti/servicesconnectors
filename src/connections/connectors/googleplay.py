""" Google play connections module """

from dataclasses import dataclass
from typing import List, Optional

import httpx
from bs4 import BeautifulSoup
from dataclasses_json import DataClassJsonMixin

from .connector import Connector, ConnectorException


class GooglePlayConnectorException(ConnectorException):
    """Base exception for GooglePlay connectors"""


def get_element_text(
    soup: BeautifulSoup, element: str, attributes: Optional[dict] = None
) -> Optional[str]:
    """Get first element text from http by attributes"""
    element = soup.find(element, attributes)
    if element is None:
        return None
    return element.text.strip()


def get_all_element_text(
    soup: BeautifulSoup, element: str, class_: Optional[str] = None
) -> Optional[List[str]]:
    """Get all element text from html by CSS class"""
    elements = soup.find_all(element, class_=class_)
    if elements is None:
        return None
    return [element.text.strip() for element in elements]


@dataclass
class GooglePlayItem(DataClassJsonMixin):
    """Google play extracted data item"""

    url: str
    itemtype: str = "googleplay"
    name: Optional[str] = None
    description: Optional[str] = None
    rating: Optional[str] = None
    reviews: Optional[str] = None


class GooglePlayConnector(Connector):
    """Google play connector"""

    def read_source(self) -> dict:
        """Read data from google play connections"""
        url = f"https://play.google.com/store/apps/details?id={self.settings['slug']}"
        response = httpx.get(url)
        if response.status_code != 200:
            raise GooglePlayConnectorException(
                f"Error: {response.status_code}", self.settings
            )

        soup = BeautifulSoup(response.text, "html.parser")

        return GooglePlayItem(
            url=url,
            name=get_element_text(soup, "h1", {"itemprop": "name"}),
            description=get_element_text(soup, "div", {"data-g-id": "description"}),
            rating=get_element_text(soup, "div", {"itemprop": "starRating"}),
            reviews=get_all_element_text(soup, "div", class_="h3YV2d"),
        ).to_dict()
