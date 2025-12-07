from module.rss import torrentRSSParser
from module.parser import openaiParser
from module.databse import RSSDatabaseManager
from module.settings import configManager

class rssManager:
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
    
    def add_rss(self, rss_link):
        self.db_manager.add_rss_source(rss_link)

    def list_rss(self):
        return self.db_manager.get_all_bangumi()

    def remove_rss(self, rss_link):
        self.db_manager.remove_rss_source(rss_link)


