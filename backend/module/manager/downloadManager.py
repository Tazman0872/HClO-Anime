from module.databse import RSSDatabaseManager
from module.settings import configManager
from module.downloader import QbDownloader

class downloadManager:
    def __init__(self):
        self.config = configManager("config/config.yaml")
        self.db_manager = RSSDatabaseManager(self.config.get("database.host"),
                                             self.config.get("database.port"),
                                             self.config.get("database.database"),
                                             self.config.get("database.user"),
                                             self.config.get("database.password"))
        self.qb_downloader = QbDownloader(self.config.get("qbittorrent.host"),
                                          self.config.get("qbittorrent.user"),
                                          self.config.get("qbittorrent.password"))
    
    def main(self):
        while True:
            self._download_episode()

    def _download_episode(self):
        bangumi_list = self.db_manager.get_all_bangumi()
        if not bangumi_list:
            return
        for bangumi in bangumi_list:
            undownloaded_episodes = self.db_manager.get_undownloaded_episodes(bangumi["bangumi_id"])
            for undownloaded_episode in undownloaded_episodes:
                if (not self.config.get("filter.hasCHS") or undownloaded_episode["haschs"]) and \
                   (not self.config.get("filter.hasCHT") or undownloaded_episode["hascht"]) and \
                   (undownloaded_episode["subtitle_type"] in self.config.get("filter.subtype")) and \
                   undownloaded_episode["parsed"]:
                    prefix = (self.config.get('qbittorrent.path_prefix') or '').rstrip('/')
                    bangumi_name = bangumi.get('bangumi_name', '')
                    season = str(undownloaded_episode.get('season', ''))
                    episode = str(undownloaded_episode.get('episode', ''))
                    target_path = f"{prefix}/{bangumi_name}/Season {season}"
                    display_name = f"{bangumi_name} S{season.zfill(2)}E{episode.zfill(2)}"

                    self.qb_downloader.add_torrents(
                        undownloaded_episode['link'],
                        None,
                        target_path,
                        None,
                        display_name
                    )
                    self.db_manager.mark_as_downloaded(bangumi["bangumi_id"], undownloaded_episode["link"])