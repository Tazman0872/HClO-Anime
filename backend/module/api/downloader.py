from fastapi import APIRouter, HTTPException, BackgroundTasks
from module.manager import downloadManager
import threading

download_manager = downloadManager()

router = APIRouter(
    prefix="/downloader",
    tags=["downloader"],
    responses={404: {"description": "Not found"}},
)

# 全局状态：控制是否已有下载任务在运行
_is_downloading = False
_downloading_lock = threading.Lock()


def _run_downloading():
    global _is_downloading
    with _downloading_lock:
        if _is_downloading:
            return
        _is_downloading = True

    try:
        download_manager.main()
    finally:
        with _downloading_lock:
            _is_downloading = False


@router.post("/main")
def add_rss(background_tasks: BackgroundTasks):
    """
    启动下载任务（确保同一时间只有一个任务运行）
    """
    global _is_downloading

    with _downloading_lock:
        if _is_downloading:
            raise HTTPException(
                status_code=429,
                detail="Download task already in progress. Please wait."
            )

    background_tasks.add_task(_run_downloading)
    return {
        "message": "Start downloading",
    }