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
        for bangumi in bangumi_list:
            undownloaded_episodes = self.db_manager.get_undownloaded_episodes(bangumi["bangumi_id"])
            for undownloaded_episode in undownloaded_episodes:
                if (not self.config.get("filter.hasCHS") or undownloaded_episode["haschs"]) and \
                   (not self.config.get("filter.hasCHT") or undownloaded_episode["hascht"]) and \
                   (undownloaded_episode["subtitle_type"] in self.config.get("filter.subtype")) and \
                   undownloaded_episode["parsed"]:
                    self.qb_downloader.add_torrents(undownloaded_episode["link"],
                                                    None,
                                                    f"{self.config.get("qbittorrent.path_prefix").rstrip("/")}/{bangumi["bangumi_name"]}/Season {str(undownloaded_episode["season"])}",
                                                    None,
                                                    f"{bangumi["bangumi_name"]} S{str(undownloaded_episode["season"]).zfill(2)}E{str(undownloaded_episode["episode"]).zfill(2)}")
                    self.db_manager.mark_as_downloaded(bangumi["bangumi_id"], undownloaded_episode["link"])