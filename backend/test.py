from module.manager import rssManager, parseManager
import logging

logging.basicConfig(level=logging.INFO)

rm = rssManager()
# rm.add_rss("https://mikanani.me/RSS/Bangumi?bangumiId=3754&subgroupid=203")
# print(rm.list_rss())
# rm.remove_rss("https://mikanani.me/RSS/Bangumi?bangumiId=3754&subgroupid=203")

pm = parseManager()
pm.main()