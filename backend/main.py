from fastapi import FastAPI
from module.api import api_router
import logging
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

logging.basicConfig(
    level=logging.INFO
)

app = FastAPI(
    title="HClO Anime API"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

uvicorn.run(app, host="127.0.0.1", port=8000)