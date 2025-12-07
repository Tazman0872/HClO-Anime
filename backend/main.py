from fastapi import FastAPI
from module.api import api_router
import logging
import uvicorn

logging.basicConfig(
    level=logging.INFO
)

app = FastAPI(
    title="HClO Anime API"
)

app.include_router(api_router)

uvicorn.run(app, host="127.0.0.1", port=8000)