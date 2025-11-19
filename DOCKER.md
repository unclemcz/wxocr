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
docker run -d \
  --name wxocr-service \
  -p 5000:5000 \
  wxocr:latest
```


## Docker配置文件说明

### 1. Dockerfile
- **基础镜像**：Python 3.13-slim
- **工作目录**：/app
- **依赖管理**：使用PDM管理Python依赖
- **Web服务器**：使用Flask内置开发服务器
- **数据持久化**：数据库和临时文件使用卷挂载

### 2. docker-compose.yml
- **服务配置**：wxocr主服务
- **卷挂载**：数据和临时文件
- **环境变量**：Flask配置和数据库路径
- **网络配置**：独立网络隔离

### 3. .dockerignore
排除不必要的文件，减少镜像大小：
- Git文件、Python缓存文件
- 开发工具配置、临时文件
- 日志文件、测试文件

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

### 数据管理

```bash
# 备份数据库
docker exec wxocr-service cp /app/data/wxocr.sqlit e /backup/

# 查看容器内文件
docker exec -it wxocr-service ls -la /app/data/

# 进入容器调试
docker exec -it wxocr-service /bin/bash
```

## 生产环境配置

### 1. 环境变量配置
创建 `.env` 文件：

```bash
# .env
FLASK_ENV=production
DATABASE=/app/data/wxocr.sqlite
# 其他自定义配置
```

### 2. 资源限制
在 docker-compose.yml 中添加资源限制：

```yaml
services:
  wxocr:
    # ... 其他配置
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M
```

### 3. 日志管理
配置日志轮转：

```yaml
services:
  wxocr:
    # ... 其他配置
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

## 故障排除

### 1. 微信OCR引擎问题
```bash
# 检查容器内微信OCR文件是否存在
docker exec wxocr-service ls -la /opt/wechat/wxocr

# 检查权限
docker exec wxocr-service ls -la /opt/wechat/

# 测试OCR引擎是否正常工作
docker exec wxocr-service /opt/wechat/wxocr --help
```

### 2. 容器启动失败
```bash
# 查看详细日志
docker-compose logs wxocr

# 检查容器状态
docker inspect wxocr-service
```

### 3. API调用失败
```bash
# 测试服务是否正常
curl http://localhost:5000/

# 检查端口映射
docker port wxocr-service
```

### 4. 数据库问题
```bash
# 重新初始化数据库
docker exec -it wxocr-service pdm run flask --app src/wxocr init-db
```

## 性能优化

### 1. 镜像优化
- 使用多阶段构建减少镜像大小
- 清理不必要的包和缓存
- 使用 .dockerignore 排除无关文件

### 2. 运行时优化
- 配置适当的超时时间
- 使用内存缓存提升性能
- 对于生产环境建议考虑使用Gunicorn等WSGI服务器

### 3. 网络优化
- 使用专用网络
- 配置适当的反向代理
- 启用HTTPS加密

## 安全建议

1. **最小权限原则**：使用非root用户运行容器
2. **网络安全**：配置防火墙规则，限制访问端口
3. **定期更新**：及时更新基础镜像和依赖包
4. **监控告警**：配置容器监控和日志告警
5. **备份策略**：定期备份数据库和配置文件

## 扩展部署

### 集群部署
使用Docker Swarm或Kubernetes进行集群部署：

```yaml
# 示例：Kubernetes Deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: wxocr-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: wxocr
  template:
    metadata:
      labels:
        app: wxocr
    spec:
      containers:
      - name: wxocr
        image: wxocr:latest
        ports:
        - containerPort: 5000
```

### 微服务架构
将OCR服务拆分为独立的微服务，配合API网关使用：

- API网关：路由和认证
- OCR服务：专注文字识别
- 认证服务：API密钥管理
- 监控服务：日志和指标收集

## 许可证

本Docker配置遵循MIT许可证，与原项目保持一致。