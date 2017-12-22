# hopapapa

API地址: https://documenter.getpostman.com/collection/view/1732102-95e440d1-eb8c-ec38-3d94-afd349e6c370

## 环境配置

环境需求：
python version=2.7.12
nginx elastic

- 进入src目录，修改local_config.py中SQLALCHEMY_DATABASE_URI为可访问库地址
- 进入根目录 执行  source env.sh
- 执行 pip install -r requirements.txt
- 执行 pip install gunicorn

## 启动流程
- source env.sh
- mysql启动
- elasticsearch 启动 /usr/local/elastic  ./bin/elasticsearch -d（切换elastic账户）
- nginx 启动 /usr/local/nginx ./sbin/nginx
- gunicorn -w 4 -b 0.0.0.0:8000 run:app

 

（除search 都在root下启动）


