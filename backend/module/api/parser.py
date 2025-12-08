from fastapi import APIRouter, BackgroundTasks, HTTPException
from module.manager import parseManager
import threading

parse_manager = parseManager()

router = APIRouter(
    prefix="/parser",
    tags=["parser"],
    responses={404: {"description": "Not found"}},
)

# 全局锁和运行状态
_parsing_lock = threading.Lock()
_is_parsing = False


def _run_parsing():
    global _is_parsing
    with _parsing_lock:
        if _is_parsing:
            # 已经在运行，直接返回（不会发生，因为调用前已检查）
            return
        _is_parsing = True

    try:
        parse_manager.main()  # 执行耗时解析
    finally:
        with _parsing_lock:
            _is_parsing = False


@router.post("/main")
def add_rss(background_tasks: BackgroundTasks):
    global _is_parsing

    with _parsing_lock:
        if _is_parsing:
            raise HTTPException(status_code=429, detail="Parsing already in progress")

    background_tasks.add_task(_run_parsing)
    return {"message": "Started parsing"}


@router.get("/status")
def parsing_status():
    """Return whether parsing is currently in progress."""
    with _parsing_lock:
        return {"is_parsing": _is_parsing}