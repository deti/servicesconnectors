""" Schemas for connections. """

from typing import Dict

from pydantic import BaseModel


class ConnectionCreate(BaseModel):
    """Connection create schema"""

    type: str
    settings: Dict[str, str]
    description: str
