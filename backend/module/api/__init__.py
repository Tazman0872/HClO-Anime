from . import editConfig, rss, parser, downloader
from fastapi import APIRouter

# 创建一个主路由，用于挂载所有子路由
api_router = APIRouter()

# 将各个模块的路由挂载到主路由上
api_router.include_router(editConfig.router)
api_router.include_router(rss.router)
api_router.include_router(parser.router)
api_router.include_router(downloader.router)
