import json
import os
import re

from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from astrbot.api.message_components import Record


@register(
    "astrbot_plugin_keyword_voice",
    "Jaeu7",
    "关键词检测插件，检测到关键词自动发送自定义语音回复",
    "1.0.0",
    "https://github.com/Jaeu7/astrbot_plugin_keyword_voice",
)
class KeywordVoicePlugin(Star):
    def __init__(self, context: Context, config: dict | None = None):
        super().__init__(context, config)
        self.config = config or {}
        self.keyword_patterns = {}
        self.voices_dir = ""

    def _parse_config(self):
        self.enable = self.config.get("enable", True)
        self.debug_mode = self.config.get("debug_mode", False)
        self.fallback_to_text = self.config.get("fallback_to_text", True)

        voices_dir_name = self.config.get("voices_dir", "voices")
        self.voices_dir = os.path.join(os.path.dirname(__file__), voices_dir_name)

        mapping_str = self.config.get("keyword_voice_mapping", "{}")
        try:
            keyword_voice_map = json.loads(mapping_str)
            if isinstance(keyword_voice_map, dict):
                self.keyword_patterns = {}
                for kw, voice_file in keyword_voice_map.items():
                    pattern = re.compile(re.escape(kw))
                    self.keyword_patterns[pattern] = voice_file
                if self.debug_mode:
                    logger.info(f"已加载 {len(self.keyword_patterns)} 个关键词映射")
            else:
                logger.error("keyword_voice_mapping 格式错误，应为 JSON 对象")
        except json.JSONDecodeError as e:
            logger.error(f"解析 keyword_voice_mapping 失败: {e}")

    async def initialize(self):
        self._parse_config()

        if not self.enable:
            logger.info("关键词语音插件已禁用")
            return

        os.makedirs(self.voices_dir, exist_ok=True)

        missing_files = []
        for voice_file in self.keyword_patterns.values():
            voice_path = os.path.join(self.voices_dir, voice_file)
            if not os.path.exists(voice_path):
                missing_files.append(voice_file)

        if missing_files:
            logger.warning(f"以下语音文件缺失，请上传到 {self.voices_dir}: {', '.join(missing_files)}")
        else:
            logger.info(f"关键词语音插件已加载，共 {len(self.keyword_patterns)} 个关键词，所有语音文件就绪")

    @filter.regex(r".*")
    async def on_message(self, event: AstrMessageEvent):
        if not self.enable:
            return

        message_str = event.message_str.strip()
        if not message_str:
            return

        for pattern, voice_file in self.keyword_patterns.items():
            if pattern.search(message_str):
                voice_path = os.path.join(self.voices_dir, voice_file)

                if self.debug_mode:
                    logger.info(f"检测到关键词 '{pattern.pattern}'，发送语音: {voice_file}")

                if os.path.exists(voice_path):
                    record = Record.fromFileSystem(voice_path)
                    yield event.chain_result([record])
                else:
                    logger.warning(f"语音文件不存在: {voice_path}")
                    if self.fallback_to_text:
                        yield event.plain_result(f"[语音文件缺失: {voice_file}]")
                return

    async def terminate(self):
        logger.info("关键词语音插件已卸载")
