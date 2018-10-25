### 数据吗迁移命令
* python manage.py db init
* python manage.py db migrate
* python manage.py db upgrade

### 定时任务crontab
```bash
SHELL=/bin/bash
LANG=en_US.utf8

# jeanfo_ask 知乎爬虫
45 12 * * 1-5 cd /data/releases/jeanfo_ask && python manage.py zhihu_scrapy >> /data/var/log/jeanfo_ask/cr
on_zhihu_scrapy.log 2>&1
```

### uwsgi.ini
```text
[uwsgi]
# uwsgi启动时所使用的地址与端口
socket = 127.0.0.1:8000
;http = 0.0.0.0:8000

# 网站根目录
chdir = /data/releases/jeanfo_ask

# python启动程序文件
wsgi-file = manage.py

# python程序内用于启动的application变量名
callable = app

processes = 2
threads = 2

# 状态监测地址
stats = 127.0.0.1:8100

# 设置uwsgi包解析的内部缓存区大小，默认4k
buffer-size = 32768
```

### supervisor conf
```text
[program:jeanfo_ask]
command=/usr/bin/uwsgi /data/releases/jeanfo_ask/uwsgi.ini

directory=/data/releases/jeanfo_ask
user=jeanfo

autostart=true
autorestart=true

stdout_logfile=/data/var/log/jeanfo_ask/uwsgi_supervisor.log
```

### nginx conf
```text
server {
  listen 80;
  server_name ask.jeanfo.cn;

  location / {
    include uwsgi_params;
    uwsgi_pass 127.0.0.1:8000;
    uwsgi_param UWSGI_CHDIR /data/releases/jeanfo_ask;
    uwsgi_param UWSGI_SCRIPT manage:app;
  }
}
```