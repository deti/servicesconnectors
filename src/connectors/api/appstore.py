""" Appstore integration """

import httpx
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from src.connectors.models import get_or_create_connector
from src.connectors.schemas import ConnectorCreate
from src.dependencies import get_db

router = APIRouter()


class AppStoreItem(BaseModel):
    """AppStore input paramters"""

    region: str = Field(title="region", description="Region of the app")
    slug: str = Field(title="slug", description="Slug of the app")
    appid: str = Field(title="appid", description="App id of the app")
    description: str = Field(description="Description of the item", max_length=100)


def build_appstore_url(item: AppStoreItem) -> str:
    """Build an AppStore application URL"""
    return f"https://apps.apple.com/{item.region}/app/{item.slug}/{item.appid}"


@router.post("/appstore")
async def create_appstore_connector(item: AppStoreItem, db: Session = Depends(get_db)):
    """Create an AppStore connector"""

    # verify that resource exists
    url = build_appstore_url(item)

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found"
            )

    connector_create = ConnectorCreate(
        connector_type="appstore",
        connector_settings={
            "connector_type": "appstore",
            "region": item.region,
            "slug": item.slug,
            "appid": item.appid,
        },
        description=item.description,
    )
    connector = get_or_create_connector(db, connector_create)

    return {
        "connector_type": "appstore",
        "message": f"Created '{item.description}'",
        "uuid": connector.uuid,
    }
