""" Main for connections application. """

from fastapi import FastAPI

from src.connections.api import router as connections_router

app = FastAPI()

app.include_router(connections_router)


@app.get("/")
async def root():
    """Root endpoint for testing purposes"""
    return {"message": "alive"}
