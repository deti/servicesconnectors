""" Connections read update delete operations """

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.connections.models import (delete_connection_from_db,
                                   get_all_connections, get_connection)
from src.connections.runner import run_connector
from src.connections.storage import Storage
from src.dependencies import get_db

router = APIRouter()


@router.get("/")
def get_all_configured_connections(db: Session = Depends(get_db)):
    """Get all connections configured across the system"""
    return get_all_connections(db)


@router.get(
    "/{uuid}",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Connection not found",
            "content": {
                "application/json": {"example": {"detail": "Connection not found"}}
            },
        },
        status.HTTP_204_NO_CONTENT: {
            "description": "Connection is not fetched yet",
            "content": None,
        },
    },
)
async def read_connection_data(uuid: str, db: Session = Depends(get_db)):
    """Read a connection data"""

    # verify that resource exists in database
    connection = get_connection(db, uuid)

    if connection is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Connection not found"
        )

    storage = Storage()
    item = storage.read(uuid)
    if item is None:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)

    return item


@router.delete("/{uuid}")
async def delete_connection(uuid: str, db: Session = Depends(get_db)):
    """Delete a connection"""
    # verify that resource exists in database
    connection = get_connection(db, uuid)
    if connection is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Connection not found"
        )

    delete_connection_from_db(db, uuid)
    storage = Storage()
    storage.delete(uuid)
    return {"message": f"Deleted {uuid}"}


@router.put("/{uuid}")
async def update_connection_data(uuid: str, db: Session = Depends(get_db)):
    """Update a connection data"""
    # verify that resource exists in database
    connection = get_connection(db, uuid)
    if connection is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Connection not found"
        )

    run_connector(connection)
    return {"message": f"Updated {connection.uuid}"}
