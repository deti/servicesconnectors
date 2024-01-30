""" Connector read update delete operations """

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.connectors.models import all_connectors_uuids, get_connector
from src.connectors.storage import Storage
from src.dependencies import get_db

router = APIRouter()


@router.get("/")
def get_all_connectors_uuids(db: Session = Depends(get_db)):
    """Get all connectors"""
    return {"uuids": all_connectors_uuids(db)}


@router.get(
    "/{uuid}",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Connector not found",
            "content": {
                "application/json": {"example": {"detail": "Connector not found"}}
            },
        },
        status.HTTP_204_NO_CONTENT: {
            "description": "Connector is not fetched yet",
            "content": {
                "application/json": {
                    "example": {"detail": "Connector is not fetched yet"}
                }
            },
        },
    },
)
async def read_appstore_connector(uuid: str, db: Session = Depends(get_db)):
    """Read a connector data"""

    # verify that resource exists in database
    connector = get_connector(db, uuid)

    if connector is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Connector not found"
        )

    storage = Storage()
    item = storage.read(uuid)
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT, detail="Connector not fetched yet"
        )

    return item
