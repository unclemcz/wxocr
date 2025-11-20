# 使用Python 3.13官方镜像作为基础镜像
FROM python:3.13-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    FLASK_APP=src/wxocr/__init__.py \
    FLASK_ENV=production \
    DATABASE=/app/data/wxocr.sqlite


# 安装PDM
RUN pip install --no-cache-dir pdm

# 复制微信安装包和项目文件
COPY WeChatLinux_x86_64.deb /tmp/WeChatLinux_x86_64.deb
COPY pyproject.toml pdm.lock README.md ./
COPY src/ ./src/

# 安装Python依赖
RUN pdm install --prod 

# 安装系统依赖和微信Linux
RUN apt-get update && apt-get install -y \
    fonts-noto-cjk \
    libglib2.0-0 \
    libstdc++6 \
    libgcc-s1 \
    libc6 \
    libz1 \
    libexpat1 \
    && dpkg -i /tmp/WeChatLinux_x86_64.deb \
    && apt-get install -f -y \
    && rm -rf /tmp/WeChatLinux_x86_64.deb \
    && rm -rf /var/lib/apt/lists/* \
    # 清理微信不必要的文件以减小镜像大小
    && echo "开始清理微信不必要的文件..." \
    && rm -rf /opt/wechat/RadiumWMPF \
    && rm -rf /opt/wechat/vlc_plugins \
    && rm -rf /opt/wechat/XEditor \
    && rm -rf /opt/wechat/XFile \
    && rm -rf /opt/wechat/wechat \
    && rm -rf /opt/wechat/libvoipCodec.so \
    && rm -rf /opt/wechat/libWxVcodec2Dyn.so \
    && echo "微信文件清理完成"

# 创建数据目录和临时文件目录
RUN mkdir -p /app/data /app/temp

# 初始化数据库
RUN pdm run flask --app src/wxocr init-db

# 暴露端口
EXPOSE 5000

# 设置启动命令
CMD ["pdm", "run", "flask", "--app", "src.wxocr", "run", "--host=0.0.0.0", "--port=5000"]