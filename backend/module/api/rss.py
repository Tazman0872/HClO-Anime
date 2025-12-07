from fastapi import APIRouter, HTTPException, BackgroundTasks
from module.manager import rssManager

rss_manager = rssManager()

router = APIRouter(
    prefix="/rss",
    tags=["rss"],
    responses={404: {"description": "Not found"}},
)


@router.post("/add")
def add_rss(rss_link: str, background_tasks: BackgroundTasks):
    """
    异步添加 RSS 源（立即返回，后台处理）
    """
    rss_manager.add_rss(rss_link)
    return {
        "message": "RSS 源已加入处理队列",
        "rss_link": rss_link,
        "status": "processing"
    }

@router.get("/list")
def list_rss():
    """
    获取所有已添加的 Bangumi 列表
    """
    try:
        bangumi_list = rss_manager.list_rss()
        return bangumi_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取 RSS 列表失败: {str(e)}")


@router.delete("/remove")
def remove_rss(rss_link: str):
    """
    删除指定的 RSS 源
    """
    try:
        rss_manager.remove_rss(rss_link)
        return {"message": "RSS 源删除成功", "rss_link": rss_link}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除 RSS 源失败: {str(e)}")