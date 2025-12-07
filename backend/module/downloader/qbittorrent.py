import logging
import time
from qbittorrentapi import Client, LoginFailed
from qbittorrentapi.exceptions import (
    APIConnectionError,
    Conflict409Error,
    Forbidden403Error,
)

logger = logging.getLogger(__name__)

class QbDownloader:
    def __init__(self, host: str, username: str, password: str, ssl: bool=False):
        self._client: Client = Client(
            host=host,
            username=username,
            password=password,
            VERIFY_WEBUI_CERTIFICATE=ssl,
            DISABLE_LOGGING_DEBUG_OUTPUT=True,
            REQUESTS_ARGS={"timeout": (3.1, 10)},
        )
        self.host = host
        self.username = username

    def auth(self, retry=3):
        times = 0
        while times < retry:
            try:
                self._client.auth_log_in()
                return True
            except LoginFailed:
                logger.error(
                    f"Can't login qBittorrent Server {self.host} by {self.username}, retry in {5} seconds."
                )
                time.sleep(5)
                times += 1
            except Forbidden403Error:
                logger.error("Login refused by qBittorrent Server")
                logger.info("Please release the IP in qBittorrent Server")
                break
            except APIConnectionError:
                logger.error("Cannot connect to qBittorrent Server")
                logger.info("Please check the IP and port in WebUI settings")
                time.sleep(10)
                times += 1
            except Exception as e:
                logger.error(f"Unknown error: {e}")
                break
        return False

    def logout(self):
        self._client.auth_log_out()

    def add_torrents(self, torrent_urls, torrent_files, save_path, category, rename):
        resp = self._client.torrents_add(
            is_paused=False,
            urls=torrent_urls,
            torrent_files=torrent_files,
            save_path=save_path,
            category=category,
            rename=rename,
            use_auto_torrent_management=False,
            content_layout="NoSubFolder"
        )
        return resp == "Ok."
