""" Appstore connector for data syncronization """

from dataclasses import dataclass
from typing import List, Optional

import httpx
from bs4 import BeautifulSoup
from dataclasses_json import DataClassJsonMixin

from .connector import Connector, ConnectorException


class AppStoreConnectorException(ConnectorException):
    """Base exception for Appstore connectors"""


def get_element_text(
    soup: BeautifulSoup, element: str, class_: Optional[str] = None
) -> Optional[str]:
    """Get first element text from http by CSS class"""
    element = soup.find(element, class_=class_)  # type: ignore
    if element is None:
        return None
    return element.text.strip()  # type: ignore


def get_all_element_text(
    soup: BeautifulSoup, element: str, class_: Optional[str] = None
) -> Optional[List[str]]:
    """Get all element text from http by CSS class"""
    elements = soup.find_all(element, class_=class_)
    if elements is None:
        return None
    return [element.text.strip() for element in elements]


@dataclass
class AppStoreItem(DataClassJsonMixin):  # pylint: disable=too-many-instance-attributes
    """Appstore extracted data item"""

    item_uuid: str
    type: str
    url: str
    title: Optional[str] = None
    subtitle: Optional[str] = None
    company: Optional[str] = None
    price: Optional[str] = None
    description: Optional[str] = None
    whats_new: Optional[str] = None
    rating: Optional[str] = None
    reviews: Optional[str] = None


class AppstoreConnector(Connector):
    """Connector for AppStore"""

    def read_source(self) -> dict:
        """Read source data from AppStore"""
        url = (
            f"https://apps.apple.com/{self.settings['region']}"
            f"/app/{self.settings['slug']}/"
            f"{self.settings['appid']}"
        )
        with httpx.Client() as client:
            response = client.get(url)
            if response.status_code != 200:
                raise AppStoreConnectorException(
                    f"Error: {response.status_code}", self.settings
                )

        soup = BeautifulSoup(response.text, "html.parser")

        item = AppStoreItem(
            item_uuid=str(self.item_uuid),
            type="appstore",
            url=url,
            title=get_element_text(soup, "h1", "product-header__title"),
            subtitle=get_element_text(soup, "h2", "product-header__subtitle"),
            company=get_element_text(soup, "h2", "product-header__identity"),
            price=get_element_text(soup, "li", "app-header__list__item--price"),
            description=get_element_text(soup, "div", "section__description"),
            whats_new=get_element_text(soup, "div", "whats-new__content"),
            rating=get_element_text(
                soup, "span", "we-customer-ratings__averages__display"
            ),
            reviews=get_all_element_text(
                soup, "div", "we-customer-review"  # type: ignore
            ),
        )

        return item.to_dict()
