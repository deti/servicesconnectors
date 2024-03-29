""" Appstore integration """

import httpx
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from src.connections.models import get_or_create_connection
from src.connections.schemas import ConnectionCreate
from src.dependencies import get_db

router = APIRouter()


class AppStoreConnectionItem(BaseModel):
    """AppStore connections creation input paramters"""

    region: str = Field(title="region", description="Region of the app")
    slug: str = Field(title="slug", description="Slug of the app")
    appid: str = Field(title="appid", description="App id of the app")
    description: str = Field(description="Description of the item", max_length=100)


def build_appstore_url(item: AppStoreConnectionItem) -> str:
    """Build an AppStore application URL"""
    return f"https://apps.apple.com/{item.region}/app/{item.slug}/{item.appid}"


@router.post("/appstore")
async def create_appstore_connection(
    item: AppStoreConnectionItem, db: Session = Depends(get_db)
):
    """Create an AppStore connection"""

    # verify that resource exists
    url = build_appstore_url(item)

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found"
            )

    connection_create = ConnectionCreate(
        type="appstore",
        settings={
            "type": "appstore",
            "region": item.region,
            "slug": item.slug,
            "appid": item.appid,
        },
        description=item.description,
    )
    connection = get_or_create_connection(db, connection_create)

    return {
        "type": "appstore",
        "message": f"Created '{item.description}'",
        "uuid": connection.uuid,
    }
