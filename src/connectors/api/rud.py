""" Connector read update delete operations """

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.connectors.models import all_connectors_uuids
from src.dependencies import get_db

router = APIRouter()


@router.get("/")
def get_all_connectors_uuids(db: Session = Depends(get_db)):
    """Get all connectors"""
    return {"uuids": all_connectors_uuids(db)}
