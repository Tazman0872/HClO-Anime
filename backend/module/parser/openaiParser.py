from openai import OpenAI
import json, logging

parseInfoSystemPrompt = """
你是一位元数据提取专家，仅根据文件名提取结构化信息，输出标准 JSON, **禁止推测、补全或使用外部知识**。

**提取规则：**
1. **`hasCHS` / `hasCHT`**：布尔值。仅当文件名含以下关键词时为 `true`:  
   - 简体：`简体`、`简`、`CHS`、`GB`、`Simplified`  
   - 繁体：`繁体`、`繁`、`CHT`、`BIG5`、`Traditional`  
   - 仅写“中文字幕”“内封字幕”等模糊词 → `false`

2. **`subtitle_type`**：仅允许 `HRD`、`SFT`、`EXT`、`UKN`  
   - `HRD`：`硬字幕`、`内嵌`、`HRD`、`Burned`  
   - `SFT`：`软字幕`、`内封`、`SFT`、`MKV`、`MP4`（含字幕流）、`多语`（若含字幕流）  
   - `EXT`：`.srt`、`.ass`、`.sub`、`外挂`、`字幕包`  
   - `UKN`：其他（含仅提“字幕”但无类型）

3. **`season` / `episode`**：整数或 `null`  
   - 匹配：`第X季`、`S01`、`Season 1`；`第X集`、`E05`、`Episode 5`、`05`  
   - 未标注季默认第一季
   - 合集/多集/OVA/剧场版 → `null, null`  
   - 未标注 → `1, null`（默认第一季，无集数）

**输出格式（严格）：**  

{"hasCHS":true/false,"hasCHT":true/false,"subtitle_type":"HRD|SFT|EXT|UKN","season":整数或null,"episode":整数或null}


> ⚠️ 仅基于文件名文本判断。模糊、缺失、未明确 → `false` 或 `null`。禁止添加任何额外内容, **严禁**使用markdown格式!
"""

parseNameSystemPrompt = """
你是一个专业的元数据提取专家，任务是从输入的字符串中精准提取出**剧集的正式名称**（不包含制作组、季数、集数、特殊符号或附加信息）。

请遵循以下规则：
1. 仅返回剧集的主标题，**不包含任何前缀、后缀、季号、制作组名、括号内容或标点符号**。
2. 若输入中包含“第X季”、“Sx”、“Season X”、“EP”、“集”等标识，必须**完全忽略**。
3. 若输入中包含制作组名称（如“Mikan Project -”、“Studio XYZ”等），必须**剔除**。
4. 输出必须**仅包含剧集名称**，无需引号、空格或任何其他字符。

**示例：**  
输入：`Mikan Project - 间谍过家家 第三季`  
输出：`间谍过家家`

**再举一例：**  
输入：`[ACG字幕组] 鬼灭之刃 无限列车篇 S2`  
输出：`鬼灭之刃`
"""

class openaiParser():
    def __init__(self, url: str, model: str, api_key: str):
        self.client = OpenAI(api_key=api_key,
                            base_url=url)
        self.model = model
        self.logger = logging.getLogger(__name__)
        self.logger.debug(f"using openai api with url:{url}, api key:{api_key}")
        
    def _getResponse(self, prompt: str, systemPrompt: str=""):
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": systemPrompt},
                    {"role": "user", "content": prompt},
                ],
                stream=False
            )
            return response.choices[0].message.content
        except:
            self.logger.error(f"cannot use AI parser, check your AI parser settings")
            return None
    
    def parseFile(self, bangumiName: str):
        response = self._getResponse(bangumiName, parseInfoSystemPrompt)
        try:
            return json.loads(response) if response else self.logger.error("no responce from openai")
        except:
            self.logger.error(f"AI parser recieved unstructured data:{response}")
    
    def parseName(self, bangumiName: str):
        response = self._getResponse(bangumiName, parseNameSystemPrompt)
        return response

if __name__ == "__main__":
    api_key = "sk-dcf206c250064b759b862bf47bedcf18"

    parser = openaiParser("https://api.deepseek.com", "deepseek-chat", api_key)
    print(parser.parseFile("[银色子弹字幕组][名侦探柯南][第1182集 抓住那个长相的人][WEBRIP][简繁日多语MKV][PGS][1080P]"))