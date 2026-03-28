# NSFW Detector

> Fork版本
> 较原版
> - 新增auth认证请求头
> - 使用环境变量配置(移除config配置文件)
> - 新增docker-compose.yml部署
> - 修复dockerfile过期依赖

## 简介

这是一个 NSFW 内容检测器，它基于 [Falconsai/nsfw_image_detection](https://huggingface.co/Falconsai/nsfw_image_detection) 。
模型: google/vit-base-patch16-224-in21k

现在同时支持图片、视频自动标签分类接口，可输出如动漫、风景、少女、城市、动物等自动生成标签。

相比其它常见的 NSFW 检测器，这个检测器的优势在于：

* 基于 AI ，准确度更好。
* 支持纯 CPU 推理，可以运行在大部分服务器上。
* 自动调度多个 CPU 加速推理。
* 简单判断，只有两个类别：nsfw 和 normal。
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
| `nsfw_threshold` | `0.8` | 检测阈值 (0-1) |
| `ffmpeg_max_frames` | `20` | FFmpeg处理最大帧数 |
| `ffmpeg_max_timeout` | `1800` | FFmpeg处理超时时间 |
| `auth_token` | `None` | API 认证 token (optional) |
| `HF_ENDPOINT` | `None` | 大陆机器需配置镜像下载抱脸托管模型，推荐https://hf-mirror.com (optional) |


### 使用内置的 Web 界面进行检测

访问地址：[http://localhost:3333](http://localhost:3333)

### 使用 API 进行内容检查

```bash
# 检测
curl -X POST -F "file=@/path/to/image.jpg" http://localhost:3333/check

# 检查本地的文件
curl -X POST -F "path=/path/to/image.jpg" http://localhost:3333/check
```

### 使用 API 进行自动标签分类

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
      {"key": "anime", "label": "动漫", "score": 0.9123},
      {"key": "girl", "label": "少女", "score": 0.8642},
      {"key": "portrait", "label": "人像", "score": 0.6211}
    ]
  }
}
```

视频返回会额外包含 `frames_analyzed` 字段，表示参与聚合分类的视频帧数量。

### 自动标签分类相关环境变量

| Option | Default | Description |
|--------|---------|-------------|
| `TAG_TOP_K` | `8` | 自动标签接口最多返回多少个标签 |
| `TAG_MIN_SCORE` | `0.2` | 自动标签接口最小分数阈值 |

## 许可证

本项目基于 Apache 2.0 许可证开源。
