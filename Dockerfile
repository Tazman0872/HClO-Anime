# ==============================
# Stage 1: 构建前端 (Vite + Vue)
# ==============================
FROM node:22-alpine AS frontend-builder

WORKDIR /app/webui
COPY webui/package*.json ./
RUN npm ci --silent
COPY webui/ .
RUN npm run build

# ==============================
# Stage 2: 构建最终镜像（Python + Nginx）
# ==============================
FROM python:3.14-slim

# 安装 Nginx
RUN apt-get update && apt-get install -y \
    nginx \
    && rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /app

# 复制 Python 依赖并安装
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制后端代码
COPY backend/ ./backend/

# 复制前端构建产物
COPY --from=frontend-builder /app/webui/dist /var/www/html
RUN rm /var/www/html/index.nginx-debian.html

# 复制 Nginx 配置（稍后创建）
COPY nginx.conf /etc/nginx/nginx.conf

# 复制启动脚本
COPY start.sh /start.sh
RUN chmod +x /start.sh

# 复制全局配置文件（供后端使用）
COPY config/config.yaml /app/config.yaml

# 暴露端口（Nginx 用 80，后端 API 假设监听 8000）
EXPOSE 80

# 启动脚本：同时启动 Nginx 和 Python 后端
CMD ["/start.sh"]