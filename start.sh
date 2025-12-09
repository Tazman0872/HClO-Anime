#!/bin/bash
set -e

# 启动 Nginx
nginx

# 启动 Python 后端（监听所有接口，端口 8000）
cd /app/backend
python main.py --host 0.0.0.0 --port 8000 &

# 保持容器运行（等待任意前台进程）
wait