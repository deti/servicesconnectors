""" Main for connector application. """

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    """Root endpoint for testing purposes"""
    return {"message": "Hello World"}
