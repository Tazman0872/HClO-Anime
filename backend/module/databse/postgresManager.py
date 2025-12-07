import hashlib
import psycopg2
import logging
from psycopg2 import sql
from typing import Optional, List, Dict, Tuple

logger = logging.getLogger(__name__)

class RSSDatabaseManager:
    def __init__(self, host, port, dbname, user, password):
        self.conn_params = {
            'host': host,
            'port': port,
            'dbname': dbname,
            'user': user,
            'password': password
        }
        self.conn = None
        self._connect()
        self._create_tables()

    def _connect(self):
        try:
            self.conn = psycopg2.connect(**self.conn_params)
            self.conn.autocommit = True
            logger.info("Successfully connected to the database.")
        except Exception as e:
            logger.error(f"Failed to connect to database: {e}")

    def _create_tables(self):
        """创建主表 rss_main（如果不存在）"""
        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS rss_main (
                        id SERIAL PRIMARY KEY,
                        link TEXT NOT NULL UNIQUE,
                        bangumi_id TEXT DEFAULT NULL,
                        bangumi_name TEXT DEFAULT NULL
                    );
                """)
            logger.debug("Ensured main table 'rss_main' exists.")
        except Exception as e:
            logger.error(f"Error creating main table: {e}")

    def _generate_bangumi_id(self, bangumi_name: str) -> str:
        """根据番剧名生成 bangumi_id（SHA256 hex）"""
        return hashlib.sha256(bangumi_name.encode('utf-8')).hexdigest()

    def _ensure_bangumi_table(self, bangumi_id: str):
        """确保为 bangumi_id 创建对应的子表（表名：rss_<bangumi_id>）"""
        table_name = f"rss_{bangumi_id}"
        try:
            with self.conn.cursor() as cur:
                cur.execute(sql.SQL("""
                    CREATE TABLE IF NOT EXISTS {} (
                        link TEXT PRIMARY KEY,
                        filename TEXT,
                        subtitle_type TEXT DEFAULT NULL,
                        hasCHS BOOLEAN DEFAULT NULL,
                        hasCHT BOOLEAN DEFAULT NULL,
                        season INTEGER DEFAULT NULL,
                        episode INTEGER DEFAULT NULL,
                        parsed BOOLEAN DEFAULT FALSE,
                        downloaded BOOLEAN DEFAULT FALSE
                    );
                """).format(sql.Identifier(table_name)))
            logger.debug(f"Ensured table '{table_name}' exists.")
        except Exception as e:
            logger.error(f"Error ensuring table '{table_name}': {e}")

    def add_rss_source(self, link: str) -> bool:
        """
        向主表添加 RSS 源
        返回生成的 bangumi_id
        """
        logger.debug(f"Adding RSS source: {link}")
        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO rss_main (link)
                    VALUES (%s)
                    ON CONFLICT (link) DO NOTHING;
                """, (link, ))
            logger.info(f"Added/ignored RSS source: {link}")
        except Exception as e:
            logger.error(f"Failed to add RSS source {link}: {e}")
            return False
        return True
    
    def update_bangumi_info(self, link: str, bangumi_name: str):
        """
        为 rss_main 表中指定 link 的条目设置 bangumi_name 和 bangumi_id。
        如果该 link 不存在，会先插入（但通常应已存在）。
        """
        bangumi_id = self._generate_bangumi_id(bangumi_name)
        logger.debug(f"Updating bangumi info for link: {link} -> {bangumi_name} (id: {bangumi_id})")
        try:
            with self.conn.cursor() as cur:
                # 先尝试插入（如果不存在），再更新 bangumi_name/id
                # 使用 ON CONFLICT UPDATE 确保即使原来没有 bangumi_name 也能更新
                cur.execute("""
                    INSERT INTO rss_main (link, bangumi_name, bangumi_id)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (link) DO UPDATE
                    SET bangumi_name = EXCLUDED.bangumi_name,
                        bangumi_id = EXCLUDED.bangumi_id
                    WHERE rss_main.bangumi_name IS NULL OR rss_main.bangumi_name = '';
                """, (link, bangumi_name, bangumi_id))
            logger.info(f"Updated bangumi info for: {link} -> {bangumi_name}")
        except Exception as e:
            logger.error(f"Failed to update bangumi info for {link}: {e}")
        return bangumi_id
    
    def remove_rss_source(self, link: str):
        """
        根据 RSS 链接从主表中删除条目，并删除对应的番剧子表。
        """
        logger.debug(f"Attempting to remove RSS source by link: {link}")
        try:
            with self.conn.cursor() as cur:
                # 先查询 bangumi_id 和 bangumi_name
                cur.execute("SELECT bangumi_id FROM rss_main WHERE link = %s;", (link,))
                result = cur.fetchone()
                if not result:
                    logger.warning(f"No RSS source found with link: {link}")
                    return
                bangumi_id = result[0]

                # 删除主表中的条目
                cur.execute("DELETE FROM rss_main WHERE link = %s;", (link,))
                logger.info(f"Deleted RSS source from main table: {link}")

                # 删除对应的子表
                table_name = f"rss_{bangumi_id}"
                cur.execute(sql.SQL("DROP TABLE IF EXISTS {};").format(sql.Identifier(table_name)))
                logger.info(f"Dropped table: {table_name}")

        except Exception as e:
            logger.error(f"Failed to remove RSS source {link}: {e}")

    def add_episode(self,
                    bangumi_id: str,
                    link: str,
                    filename: str):
        """
        向对应番剧子表添加剧集信息
        """
        logger.debug(f"Adding episode to bangumi {bangumi_id}: {filename} ({link})")
        try:
            self._ensure_bangumi_table(bangumi_id)
            table_name = f"rss_{bangumi_id}"
            with self.conn.cursor() as cur:
                cur.execute(sql.SQL("""
                    INSERT INTO {} (link, filename)
                    VALUES (%s, %s)
                    ON CONFLICT (link) DO NOTHING
                """).format(sql.Identifier(table_name)),
                (link, filename))
            logger.debug(f"Upserted episode: {filename}")
        except Exception as e:
            logger.error(f"Failed to add episode {link} for bangumi {bangumi_id}: {e}")

    def update_episode(self,
                       bangumi_id: str,
                       link: str,
                       subtitle_type: Optional[str] = None,
                       hasCHS: Optional[bool] = None,
                       hasCHT: Optional[bool] = None,
                       season: Optional[int] = None,
                       episode: Optional[int] = None):
        """
        更新指定番剧中某剧集的信息（仅更新非 None 的字段）
        """
        logger.debug(f"Updating episode {link} in bangumi {bangumi_id}")
        table_name = f"rss_{bangumi_id}"
        set_clauses = []
        params = []

        if subtitle_type is not None:
            set_clauses.append("subtitle_type = %s")
            params.append(subtitle_type)
        if hasCHS is not None:
            set_clauses.append("hasCHS = %s")
            params.append(hasCHS)
        if hasCHT is not None:
            set_clauses.append("hasCHT = %s")
            params.append(hasCHT)
        if season is not None:
            set_clauses.append("season = %s")
            params.append(season)
        if episode is not None:
            set_clauses.append("episode = %s")
            params.append(episode)

        if not set_clauses:
            logger.warning("No fields to update in update_episode call.")
            return

        set_clause = ", ".join(set_clauses)
        params.append(link)

        try:
            with self.conn.cursor() as cur:
                cur.execute(sql.SQL("""
                    UPDATE {} SET {} WHERE link = %s;
                """).format(sql.Identifier(table_name), sql.SQL(set_clause)), params)
            logger.info(f"Updated episode: {link}")
        except Exception as e:
            logger.error(f"Failed to update episode {link}: {e}")

    def mark_as_parsed(self, bangumi_id: str, link: str):
        """标记某条目为已解析"""
        logger.debug(f"Marking as parsed: {link} in bangumi {bangumi_id}")
        table_name = f"rss_{bangumi_id}"
        try:
            with self.conn.cursor() as cur:
                cur.execute(sql.SQL("""
                    UPDATE {} SET parsed = TRUE WHERE link = %s;
                """).format(sql.Identifier(table_name)), (link,))
            logger.info(f"Marked as parsed: {link}")
        except Exception as e:
            logger.error(f"Failed to mark as parsed {link}: {e}")

    def mark_as_downloaded(self, bangumi_id: str, link: str):
        """标记某条目为已下载"""
        logger.debug(f"Marking as downloaded: {link} in bangumi {bangumi_id}")
        table_name = f"rss_{bangumi_id}"
        try:
            with self.conn.cursor() as cur:
                cur.execute(sql.SQL("""
                    UPDATE {} SET downloaded = TRUE WHERE link = %s;
                """).format(sql.Identifier(table_name)), (link,))
            logger.info(f"Marked as downloaded: {link}")
        except Exception as e:
            logger.error(f"Failed to mark as downloaded {link}: {e}")

    def get_unparsed_episodes(self, bangumi_id: str) -> List[Dict]:
        """获取某番剧未解析的剧集列表"""
        table_name = f"rss_{bangumi_id}"
        try:
            with self.conn.cursor() as cur:
                cur.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = %s);", (table_name,))
                if not cur.fetchone()[0]:
                    logger.debug(f"Table {table_name} does not exist. Returning empty list.")
                    return []

            with self.conn.cursor() as cur:
                cur.execute(sql.SQL("""
                    SELECT link, filename, subtitle_type, hasCHS, hasCHT, season, episode
                    FROM {} WHERE parsed = FALSE;
                """).format(sql.Identifier(table_name)))
                columns = [desc[0] for desc in cur.description]
                results = [dict(zip(columns, row)) for row in cur.fetchall()]
                logger.debug(f"Retrieved {len(results)} unparsed episodes for {bangumi_id}.")
                return results
        except Exception as e:
            logger.error(f"Error fetching unparsed episodes for {bangumi_id}: {e}")
            return []

    def get_undownloaded_episodes(self, bangumi_id: str) -> List[Dict]:
        """
        获取某番剧中所有未下载的剧集列表
        """
        table_name = f"rss_{bangumi_id}"
        try:
            with self.conn.cursor() as cur:
                # 检查表是否存在
                cur.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = %s);",(table_name,))
                if not cur.fetchone()[0]:
                    logger.debug(f"Table {table_name} does not exist. Returning empty list.")
                    return []

            with self.conn.cursor() as cur:
                cur.execute(sql.SQL("""
                    SELECT link, filename, subtitle_type, hasCHS, hasCHT, season, episode, parsed
                    FROM {} WHERE downloaded = FALSE;
                """).format(sql.Identifier(table_name)))
                columns = [desc[0] for desc in cur.description]
                results = [dict(zip(columns, row)) for row in cur.fetchall()]
                logger.debug(f"Retrieved {len(results)} undownloaded episodes for {bangumi_id}.")
                return results
        except Exception as e:
            logger.error(f"Error fetching undownloaded episodes for {bangumi_id}: {e}")
            return []

    def get_all_bangumi(self) -> List[Dict]:
        """返回主表中所有番剧信息"""
        try:
            with self.conn.cursor() as cur:
                cur.execute("SELECT id, link, bangumi_id, bangumi_name FROM rss_main;")
                columns = [desc[0] for desc in cur.description]
                results = [dict(zip(columns, row)) for row in cur.fetchall()]
                logger.debug(f"Retrieved {len(results)} bangumi entries.")
                return results
        except Exception as e:
            logger.error(f"Error fetching all bangumi: {e}")

    def close(self):
        if self.conn:
            self.conn.close()
            logger.info("Database connection closed.")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()