from fastapi import APIRouter
from module.settings import configManager

config = configManager('config/config.yaml')

# 创建一个独立的路由实例
router = APIRouter(
    prefix="/settings",
    tags=["settings"],
    responses={404: {"description": "Not found"}},
)

@router.get("/get")
def getConfig(configName: str):
    return config.get(configName)

@router.post("/set")
def getConfig(configName: str, configValue):
    config.set(configName, configValue)
    config.save()
    config.reload()
    return True
