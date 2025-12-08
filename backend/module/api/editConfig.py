from fastapi import APIRouter
from pydantic import BaseModel
from typing import Any
from module.settings import configManager

config = configManager('config/config.yaml')

router = APIRouter(
    prefix="/settings",
    tags=["settings"],
    responses={404: {"description": "Not found"}},
)

class SetConfigRequest(BaseModel):
    configName: str
    configValue: Any  # 接受任意类型：str, bool, list 等

@router.get("/get")
def getConfig(configName: str):
    return config.get(configName)

@router.post("/set")
def setConfig(request: SetConfigRequest):  # ← 从 JSON body 读取
    config.set(request.configName, request.configValue)
    config.save()
    config.reload()
    return {"success": True}