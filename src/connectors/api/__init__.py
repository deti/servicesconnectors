""" Connectors API routes """

from fastapi import APIRouter

from .appstore import router as appstore_router

router = APIRouter(
    prefix="/connectors",
    tags=["connectors"],
    responses={404: {"description": "Not found"}},
)

router.include_router(appstore_router)
