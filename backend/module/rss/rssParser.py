import feedparser
import logging
import re
import requests
from typing import List, Dict, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from urllib.parse import urljoin, urlparse

class torrentRSSParser:
    """
    RSS解析器，用于从RSS源提取种子链接和文件名信息
    """
    
    def __init__(self, logger: Optional[logging.Logger] = None, timeout: int = 30):
        """
        初始化RSS解析器
        
        Args:
            logger: 可选的日志记录器实例
            timeout: 网络请求超时时间（秒）
        """
        self.logger = logger or logging.getLogger(__name__)
        self.timeout = timeout
        # 预编译正则表达式以提高性能
        self.magnet_pattern = re.compile(r'magnet:\?[^\'"\s<>\)]+')
        self.torrent_pattern = re.compile(r'https?://[^\s\'"<>]*\.torrent[^\s\'"<>]*')
        
    def parse_rss_link(self, rss_url: str, max_entries: Optional[int] = None) -> Dict:
        """
        解析RSS链接，提取文件名和torrent链接
        
        Args:
            rss_url (str): RSS订阅链接
            max_entries: 最大解析条目数，用于限制解析范围
            
        Returns:
            dict: 包含RSS名称和种子列表的字典
        """
        start_time = time.time()
        try:
            self.logger.info(f"开始解析RSS链接: {rss_url}")
            
            feed = self._parse_feed(rss_url)
            rss_title = self._get_rss_title(feed)
            
            # 限制解析条目数量以提高性能
            entries = feed.entries[:max_entries] if max_entries else feed.entries
            torrent_list = self._extract_torrent_info(entries)
            
            elapsed_time = time.time() - start_time
            self.logger.info(f"成功解析RSS，找到 {len(torrent_list)} 个条目，耗时 {elapsed_time:.2f} 秒")
            return {"RSSName": rss_title, "torrents": torrent_list}
            
        except Exception as e:
            self.logger.error(f"解析RSS时发生错误: {e}", exc_info=True)
            return {"RSSName": None, "torrents": []}
    
    def _parse_feed(self, rss_url: str) -> feedparser.FeedParserDict:
        """
        解析RSS源，使用requests获取内容后再解析
        
        Args:
            rss_url: RSS链接
            
        Returns:
            feedparser.FeedParserDict: 解析后的RSS数据
        """
        self.logger.debug(f"正在解析RSS源: {rss_url}")
        
        try:
            # 使用requests获取RSS内容，设置超时
            response = requests.get(rss_url, timeout=self.timeout)
            response.raise_for_status()
            
            # 使用feedparser解析获取到的内容
            feed = feedparser.parse(response.content)
            
            if feed.bozo:
                self.logger.warning(f"RSS解析可能存在问题: {feed.bozo_exception}")
            
            return feed
        except requests.exceptions.Timeout:
            raise Exception(f"请求RSS源超时: {rss_url}")
        except requests.exceptions.RequestException as e:
            raise Exception(f"请求RSS源失败: {e}")
    
    def _get_rss_title(self, feed: feedparser.FeedParserDict) -> str:
        """
        获取RSS源的标题
        
        Args:
            feed: 解析后的RSS数据
            
        Returns:
            str: RSS源标题
        """
        if hasattr(feed.feed, 'title'):
            return feed.feed.title.strip()
        return None
    
    def _extract_torrent_info(self, entries) -> List[Dict[str, str]]:
        """
        从RSS entries中提取种子信息
        
        Args:
            entries: RSS条目列表
            
        Returns:
            list: 种子信息列表
        """
        torrent_list = []
        
        for i, entry in enumerate(entries):
            try:
                torrent_info = self._extract_single_entry_info(entry)
                torrent_list.append(torrent_info)
            except Exception as e:
                self.logger.error(f"处理RSS条目 {i} 时发生错误: {e}", exc_info=True)
                continue
        
        return torrent_list
    
    def _extract_single_entry_info(self, entry) -> Dict[str, str]:
        """
        从单个RSS条目中提取信息
        
        Args:
            entry: RSS条目
            
        Returns:
            dict: 包含文件名和种子链接的字典
        """
        filename = self._extract_filename(entry)
        torrent_link = self._extract_torrent_link(entry)
        
        torrent_info = {
            'filename': filename,
            'torrent_link': torrent_link
        }
        
        self.logger.debug(f"提取到条目信息: 文件名={filename}, 链接={torrent_link}")
        return torrent_info
    
    def _extract_filename(self, entry) -> str:
        """
        从RSS条目中提取文件名
        
        Args:
            entry: RSS条目
            
        Returns:
            str: 文件名
        """
        if hasattr(entry, 'title'):
            filename = entry.title.strip()
            if filename:
                return filename
        
        self.logger.debug("条目中未找到有效的标题，使用默认文件名")
        return 'Unknown'
    
    def _extract_torrent_link(self, entry) -> str:
        """
        从RSS条目中提取种子链接
        
        Args:
            entry: RSS条目
            
        Returns:
            str: 种子链接，如果未找到则返回默认消息
        """
        # 方法1: 检查entry.link是否为种子链接
        link = self._find_torrent_link_in_entry_link(entry)
        if link:
            return link
        
        # 方法2: 检查RSS条目中的enclosures
        link = self._find_torrent_link_in_enclosures(entry)
        if link:
            return link
        
        # 方法3: 检查summary或description中是否包含种子链接
        link = self._find_torrent_link_in_content(entry)
        if link:
            return link
        
        self.logger.debug("在条目中未找到种子链接")
        return 'No torrent link found'
        
    def _find_torrent_link_in_entry_link(self, entry) -> Optional[str]:
        """
        从entry.link中查找种子链接
        
        Args:
            entry: RSS条目
            
        Returns:
            str: 种子链接，如果未找到则返回None
        """
        if hasattr(entry, 'link') and entry.link:
            if self._is_torrent_link(entry.link):
                self.logger.debug(f"在entry.link中找到种子链接: {entry.link}")
                return entry.link
        
        return None
    
    def _find_torrent_link_in_enclosures(self, entry) -> Optional[str]:
        """
        从enclosures中查找种子链接
        
        Args:
            entry: RSS条目
            
        Returns:
            str: 种子链接，如果未找到则返回None
        """
        if hasattr(entry, 'enclosures'):
            for enclosure in entry.enclosures:
                if (hasattr(enclosure, 'href') and 
                    self._is_torrent_link(enclosure.href)):
                    self.logger.debug(f"在enclosures中找到种子链接: {enclosure.href}")
                    return enclosure.href
        
        return None
    
    def _find_torrent_link_in_content(self, entry) -> Optional[str]:
        """
        从内容中查找种子链接
        
        Args:
            entry: RSS条目
            
        Returns:
            str: 种子链接，如果未找到则返回None
        """
        content_fields = []
        
        if hasattr(entry, 'summary'):
            content_fields.append(entry.summary)
        if hasattr(entry, 'description'):
            content_fields.append(entry.description)
        
        for content in content_fields:
            if not content:  # 跳过空内容
                continue
                
            # 查找magnet链接
            magnet_link = self._extract_magnet_link(content)
            if magnet_link:
                self.logger.debug(f"在内容中找到magnet链接: {magnet_link}")
                return magnet_link
            
            # 查找torrent链接
            torrent_link = self._extract_torrent_link_from_text(content)
            if torrent_link:
                self.logger.debug(f"在内容中找到torrent链接: {torrent_link}")
                return torrent_link
        
        return None
    
    def _is_torrent_link(self, url: str) -> bool:
        """
        判断URL是否为种子链接
        
        Args:
            url: URL字符串
            
        Returns:
            bool: 是否为种子链接
        """
        url_lower = url.lower()
        return (url_lower.endswith('.torrent') or 
                'torrent' in url_lower or 
                url_lower.startswith('magnet:'))
    
    def _extract_magnet_link(self, content: str) -> Optional[str]:
        """
        从文本中提取magnet链接
        
        Args:
            content: 文本内容
            
        Returns:
            str: magnet链接，如果未找到则返回None
        """
        if 'magnet:' not in content:
            return None
        
        matches = self.magnet_pattern.search(content)
        return matches.group(0) if matches else None
    
    def _extract_torrent_link_from_text(self, content: str) -> Optional[str]:
        """
        从文本中提取torrent链接
        
        Args:
            content: 文本内容
            
        Returns:
            str: torrent链接，如果未找到则返回None
        """
        if '.torrent' not in content:
            return None
        
        matches = self.torrent_pattern.search(content)
        return matches.group(0) if matches else None


if __name__ == "__main__":
    """
    主函数，用于测试RSS解析器
    """
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # 创建RSS解析器实例，设置超时时间为30秒
    parser = torrentRSSParser(timeout=30)
    
    # 测试RSS链接
    rss_url = "https://mikanani.me/RSS/Bangumi?bangumiId=3774&subgroupid=370"
    
    # 解析RSS，限制最多解析10个条目以提高性能
    results = parser.parse_rss_link(rss_url, max_entries=10)
    
    # 打印结果
    print(results)