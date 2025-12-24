# 项目说明

本项目是基于 RSS 和 LLM 的全自动追番整理下载工具。只需要在 [Mikan Project][mikan] 等网站上订阅番剧，就可以全自动追番。
并且整理完成的名称和目录可以直接被 [Plex][plex]、[Jellyfin][jellyfin] 等媒体库软件识别。

## HClO Anime 功能说明

- 从给定的RSS链接名中解析提取出番剧名称，如对于标题名为：
  ```
  Mikan Project - 对我垂涎欲滴的非人少女
  ```
  的RSS链接，会返回:
  ```
  对我垂涎欲滴的非人少女
  ```
  作为该RSS连接下所有内容的根文件夹名称
 - 定期检查、筛选并下载RSS连接中未被 HClO Anime 下载过的番剧，添加至外部下载器（暂仅支持qbittorrent）中。具体表现为，对于包含：
  ```
  【喵萌奶茶屋】★10月新番★[想吃掉我的非人少女 / 对我垂涎欲滴的非人少女 / 私を喰べたい、ひとでなし / Watashi wo Tabetai, Hitodenashi][01][1080p][简日双语]
  【喵萌奶茶屋】★10月新番★[想吃掉我的非人少女 / 对我垂涎欲滴的非人少女 / 私を喰べたい、ひとでなし / Watashi wo Tabetai, Hitodenashi][01][1080p][繁日双语]
  【喵萌奶茶屋】★10月新番★[想吃掉我的非人少女 / 对我垂涎欲滴的非人少女 / 私を喰べたい、ひとでなし / Watashi wo Tabetai, Hitodenashi][02][1080p][简日双语]
  ......
  【喵萌奶茶屋】★10月新番★[想吃掉我的非人少女 / 对我垂涎欲滴的非人少女 / 私を喰べたい、ひとでなし / Watashi wo Tabetai, Hitodenashi][13][1080p][繁日双语]
  ```
  的RSS链接，从语言（仅能从简中，繁中二选一）和字幕类型（内嵌、内封、外挂、未知中任选一个或多个）两个维度进行番剧的筛选，并将通过的番剧进行下载。如对于语言要求为简中，字幕不做要求的限制条件，HClO Anime 会将以下内容进行下载：
  ```
  【喵萌奶茶屋】★10月新番★[想吃掉我的非人少女 / 对我垂涎欲滴的非人少女 / 私を喰べたい、ひとでなし / Watashi wo Tabetai, Hitodenashi][01][1080p][简日双语]
  【喵萌奶茶屋】★10月新番★[想吃掉我的非人少女 / 对我垂涎欲滴的非人少女 / 私を喰べたい、ひとでなし / Watashi wo Tabetai, Hitodenashi][02][1080p][简日双语]
  ......
  【喵萌奶茶屋】★10月新番★[想吃掉我的非人少女 / 对我垂涎欲滴的非人少女 / 私を喰べたい、ひとでなし / Watashi wo Tabetai, Hitodenashi][13][1080p][简日双语]
  ```
  下载后，对文件进行移动和重命名，组成标准的、可被识别的剧集存储结构，以供本地流媒体平台进行进一步处理

## 快速开始
 - 确保你有如下项目
   1. 外部postgresql数据库，并已创建好一个空数据库和一个带有密码的账号供 HClO Anime 使用
   2. 可使用的openai api，供 HClO Anime 进行必要的解析，推荐本地部署Qwen3-30B-A3B平衡解析质量和算力消耗
   3. 可从网络访问的qbittorrent下载器，以便HClO进行下载
 - 确保你安装了docker
 - 创建一个文件夹（替换/path/to/your/config），用于持久化存储配置信息。**注意，请妥善处理该文件夹权限，因为其中内容会包含你的数据库、api和qbittorrent账号密码！！！**
   ```bash
   mkdir /path/to/your/config
   ```
 - 运行容器
   ```bash
   docker run --name hclo-anime -v /path/to/your/config:/app/config -p 80:80 -d ghcr.io/tazman0872/hclo-anime:latest
   ```
 - 部署完成！设置你的数据库、openai api和postgres数据库来使该容器可正常使用
 - 前往mikan anime获取你希望订阅的番剧特定字幕组的RSS链接，并填入 HClO Anime 的“RSS链接”页面，你应当可以看到番剧链接出现在下方，稍候片刻待解析完成，番剧名称会一并出现。


## 贡献

欢迎提供 ISSUE 或者 PR！

## Licence

[MIT licence](https://github.com/EstrellaXD/Auto_Bangumi/blob/main/LICENSE)

[mikan]: https://mikanani.me
[plex]: https://plex.tv
[jellyfin]: https://jellyfin.org
