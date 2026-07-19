# astrbot_plugin_keyword_voice

AstrBot 关键词检测插件，检测到自定义关键词后自动发送对应的语音文件。

## 功能特性

- 🎯 自定义关键词检测
- 🔊 发送自定义语音回复
- ⚙️ WebUI 可视化配置
- 🔄 热重载支持
- 📂 支持任意音频格式（MP3、WAV、AMR、OGG 等）

## 安装

将插件目录放入 AstrBot 的 `data/plugins/` 目录下

## 配置

在 AstrBot WebUI 的插件管理页面中配置：

| 配置项 | 说明 |
|--------|------|
| 启用插件 | 是否启用关键词语音回复功能 |
| 调试模式 | 启用后输出详细的关键词匹配日志 |
| 关键词-语音文件映射 | JSON 格式，key 为关键词，value 为语音文件名 |
| 语音文件目录 | 语音文件存放的目录，相对于插件目录 |
| 语音文件缺失时回退到文本 | 当语音文件不存在时，是否发送文本提示 |

### 关键词映射示例

```json
{
    "你好": "hello.mp3",
    "早上好": "good_morning.mp3",
    "晚安": "good_night.mp3",
    "谢谢": "thanks.mp3"
}
```

## 使用

1. 将语音文件上传到插件目录下的 `voices/` 文件夹
2. 在 WebUI 配置页面设置关键词与语音文件的映射
3. 保存配置，插件会自动热重载
4. 在聊天中发送关键词，触发语音回复

## 开发

```bash
# 目录结构
astrbot_plugin_keyword_voice/
├── main.py              # 插件主程序
├── metadata.yaml        # 插件元数据
├── _conf_schema.json    # 配置 schema
├── requirements.txt     # 依赖声明
├── .gitignore           # Git 忽略文件
└── voices/              # 语音文件目录
    ├── hello.mp3
    └── ...
```
