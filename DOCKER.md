# Docker 部署指南

本文档提供将 wxocr 项目制作成 Docker 镜像的完整技术指导。

## 前置要求

### 1. 微信安装包
确保项目目录中包含 `WeChatLinux_x86_64.deb` 安装包文件。Docker构建过程会自动安装微信OCR引擎到容器内的 `/opt/wechat/` 目录。


### 手动构建

1. **构建镜像**：
```bash
docker build -t wxocr:latest .
```

2. **运行容器**：

```bash
docker run -d   --name wxocr-service   -p 5000:5000   wxocr:latest
```

## 管理命令

### API密钥管理

容器运行后，可以通过exec命令管理API密钥：

```bash
# 添加API密钥
docker exec -it wxocr-service pdm run flask --app src/wxocr add-key --appname=myapp

# 列出所有API密钥
docker exec -it wxocr-service pdm run flask --app src/wxocr list-keys

# 删除API密钥
docker exec -it wxocr-service pdm run flask --app src/wxocr del-key --appname=myapp

# 清空所有API密钥
docker exec -it wxocr-service pdm run flask --app src/wxocr clear-keys
```
