# 使用Python基础镜像
FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖和cron
RUN apt-get update && apt-get install -y cron

# 复制项目文件到工作目录
COPY . .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 创建cron任务文件
RUN echo "*/5 * * * * cd /app && scrapy crawl techflow >> /var/log/cron.log 2>&1" > /etc/cron.d/scrapy-cron

# 给cron任务文件添加执行权限
RUN chmod 0644 /etc/cron.d/scrapy-cron

# 启动cron服务
CMD ["cron", "-f"]