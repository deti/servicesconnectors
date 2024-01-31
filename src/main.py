""" Main for connector application. """

from fastapi import FastAPI

from src.connections.api import router as connectors_router

app = FastAPI()

app.include_router(connectors_router)


@app.get("/")
async def root():
    """Root endpoint for testing purposes"""
    return {"message": "alive"}
