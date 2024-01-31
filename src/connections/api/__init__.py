""" Connectors API routes """

from fastapi import APIRouter

from .appstore import router as appstore_router
from .rud import router as rud_router

router = APIRouter(
    prefix="/connections",
    tags=["connections"],
    responses={404: {"description": "Not found"}},
)

router.include_router(rud_router)
router.include_router(appstore_router)
