from module.parser import openaiParser
from module.databse import RSSDatabaseManager
from module.settings import configManager
from module.rss import torrentRSSParser


class parseManager:
    def __init__(self):
        self.config = configManager("config/config.yaml")
        self.rss_parser = torrentRSSParser(timeout=300)
        self.openai_parser = openaiParser(self.config.get("openai.base_url"),
                                          self.config.get("openai.model_name"),
                                          self.config.get("openai.api_key"))
        self.db_manager = RSSDatabaseManager(self.config.get("database.host"),
                                             self.config.get("database.port"),
                                             self.config.get("database.databse"),
                                             self.config.get("database.user"),
                                             self.config.get("database.password"))
        
    def main(self):
        while True:
            self._parse_rss_link()
            self._parse_file()
    
    def _parse_rss_link(self):
        bangumi_list = self.db_manager.get_all_bangumi()
        for bangumi in bangumi_list:
            results = self.rss_parser.parse_rss_link(bangumi["link"])
            bangumi_name = self.openai_parser.parseName(results["RSSName"])
            bangumi_id = self.db_manager.update_bangumi_info(bangumi["link"], bangumi_name)
            for torrent in results["torrents"]:
                self.db_manager.add_episode(bangumi_id, torrent["torrent_link"], torrent["filename"])

    def _parse_file(self):
        bangumi_list = self.db_manager.get_all_bangumi()
        for bangumi in bangumi_list:
            unparsed_episodes = self.db_manager.get_unparsed_episodes(bangumi["bangumi_id"])
            for unparsed_episode in unparsed_episodes:
                episode_info = self.openai_parser.parseFile(unparsed_episode["filename"])
                self.db_manager.update_episode(bangumi["bangumi_id"],
                                               unparsed_episode["link"],
                                               episode_info["subtitle_type"],
                                               episode_info["hasCHS"],
                                               episode_info["hasCHT"],
                                               episode_info["season"],
                                               episode_info["episode"])
                self.db_manager.mark_as_parsed(bangumi["bangumi_id"],
                                               unparsed_episode["link"])
