# NSFW Detector

> Fork版本
> 较原版
> - 新增auth认证请求头
> - 使用环境变量配置(移除config配置文件)
> - 新增docker-compose.yml部署
> - 修复dockerfile过期依赖

## 简介

这是一个 NSFW 内容检测器，现已升级为更强的本地模型用于鉴黄与标签分类。
默认鉴黄模型为 `Freepik/nsfw_image_detector`，默认标签分类模型为 `SmilingWolf/wd-vit-tagger-v3`，标签分类使用 WD 系列专用多标签模型而不是 zero-shot CLIP。

现在同时支持图片、视频自动标签分类接口，`/tag` 会直接返回 WD 多标签模型自主识别并生成的原生标签结果，适合检索增强、素材整理与模型驱动分类流程。

相比其它常见的 NSFW 检测器，这个检测器的优势在于：

* 基于 AI ，准确度更好。
* 支持纯 CPU 推理，可以运行在大部分服务器上。
* 自动调度多个 CPU 加速推理。
* 对外接口仍保持 `nsfw` 和 `normal` 两个结果字段，内部会自动兼容更强鉴黄模型输出。
* 以 API 的方式提供服务，更方便集成到其它应用中。
* 基于 Docker 部署，便于分布式部署。
* 纯本地，保护您的数据安全。

### 性能需求

运行这个模型最多需要 2GB 的内存。不需要显卡的支持。
在同时处理大量请求时，可能需要更多的内存。

### 支持的文件类型

这个检测器支持检查的文件类型：

* ✅ 图片（已支持）
* ✅ PDF 文件（已支持）
* ✅ 视频（已支持）
* ✅ 压缩包中的文件（已支持）
* ✅ Doc,Docx（已支持）

## 快速开始

### docker compose部署（推荐）

```bash
# 1. 创建nsfw_detector目录
mkdir -p /opt/nsfw_detector && cd /opt/nsfw_detector

# 2. 下载docker-compose.yml文件
wget https://raw.githubusercontent.com/ilolioo/nsfw_detector/refs/heads/main/docker-compose.yml

# 3. 启动服务【注意docker-compose.yml文件中支持的环境变量】
docker compose up -d
```

### docker部署（不推荐）

```bash
docker run -d -p 3333:3333 --name nsfw-detector ilolioo/nsfw_detector:latest
```
支持的系统架构：`x86_64`、`ARM64(此版本未构建)`

### 环境变量

| Option | Default | Description |
|--------|---------|-------------|
| `NSFW_THRESHOLD` | `0.8` | 检测阈值 (0-1) |
| `NSFW_MODEL_RESET_THRESHOLD` | `10000` | 鉴黄模型重置阈值 |
| `TAG_MODEL_RESET_THRESHOLD` | `5000` | 标签模型重置阈值 |
| `WD_GENERAL_THRESHOLD` | `0.32` | WD 通用标签阈值 |
| `WD_CHARACTER_THRESHOLD` | `0.80` | WD 角色标签阈值 |
| `FFMPEG_MAX_FRAMES` | `20` | FFmpeg处理最大帧数 |
| `FFMPEG_MAX_TIMEOUT` | `1800` | FFmpeg处理超时时间 |
| `AUTH_TOKEN` | `None` | API 认证 token (optional) |
| `HF_ENDPOINT` | `None` | 大陆机器需配置镜像下载抱脸托管模型，推荐https://hf-mirror.com (optional) |


### 使用内置的 Web 界面进行检测

访问地址：[http://localhost:3333](http://localhost:3333)

API 文档页面：[http://localhost:3333/api-docs](http://localhost:3333/api-docs)

首页已内置 API 文档入口，可直接跳转查看 `/check` 与 `/tag` 的请求参数、鉴权说明和响应示例。

### 使用 API 进行内容检查

如已配置 `auth_token`，请求时请在 Header 中携带：`Authorization: Bearer <token>`

```bash
# 检测
curl -X POST -F "file=@/path/to/image.jpg" http://localhost:3333/check

# 检查本地的文件
curl -X POST -F "path=/path/to/image.jpg" http://localhost:3333/check
```

### 使用 API 进行自动标签分类

`/tag` 返回的是 WD 模型原生生成的标签，不再强制映射为人工预设的内容分类标签。

```bash
# 上传图片或视频进行标签分类
curl -X POST -F "file=@/path/to/image.jpg" http://localhost:3333/tag

# 检查服务器本地文件
curl -X POST -F "path=/path/to/video.mp4" http://localhost:3333/tag
```

返回示例：

```json
{
  "status": "success",
  "filename": "sample.jpg",
  "result": {
    "type": "image",
    "tags": [
      {"key": "1girl", "label": "1girl", "score": 0.9984},
      {"key": "solo", "label": "solo", "score": 0.9961},
      {"key": "long hair", "label": "long hair", "score": 0.9418}
    ]
  }
}
```

视频返回会额外包含 `frames_analyzed` 字段，表示参与聚合分类的视频帧数量。

### 自动标签分类相关环境变量

| Option | Default | Description |
|--------|---------|-------------|
| `TAG_MODEL_RESET_THRESHOLD` | `5000` | 标签模型重置阈值 |
| `WD_GENERAL_THRESHOLD` | `0.32` | WD 通用标签阈值 |
| `WD_CHARACTER_THRESHOLD` | `0.80` | WD 角色标签阈值 |
| `TAG_TOP_K` | `16` | 自动标签接口最多返回多少个标签 |
| `TAG_MIN_SCORE` | `0.15` | 自动标签接口最小分数阈值 |

## 许可证

本项目基于 Apache 2.0 许可证开源。
