""" Google play connection API """

import httpx
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from src.connections.models import get_or_create_connection
from src.connections.schemas import ConnectionCreate
from src.dependencies import get_db

router = APIRouter()


class GooglePlayConnectionItem(BaseModel):
    """GooglePlay connections creation input paramters"""

    slug: str = Field(title="slug", description="Slug of the app")
    description: str = Field(description="Description of the item", max_length=100)


def build_googleplay_url(item: GooglePlayConnectionItem) -> str:
    """Build an AppStore application URL"""
    return f"https://play.google.com/store/apps/details?id={item.slug}"


@router.post("/googleplay")
def create_googpleplay_connection(
    item: GooglePlayConnectionItem, db: Session = Depends(get_db)
):
    """Create an AppStore connection"""

    # verify that resource exists
    url = build_googleplay_url(item)

    response = httpx.get(url)
    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found"
        )

    connection_create = ConnectionCreate(
        type="googleplay",
        settings={
            "type": "googleplay",
            "slug": item.slug,
        },
        description=item.slug,
    )
    connection = get_or_create_connection(db, connection_create)

    return {
        "type": "googleplay",
        "message": f"Created '{item.description}'",
        "uuid": connection.uuid,
    }
