# Docker を立ち上げるやつ
up:
	docker compose up -d

# app.py いじった後にコンパイルするやつ
run:
	docker-compose rm -fsv app
	docker compose up -d
	docker compose exec app pip install flask_sqlalchemy

# データベースに入るやつ
# 例: psql -h flask_db -U ${DB_USER} -d ${DB_NAME}
db-in:
	docker-compose exec database bash

# アプリコンテナに入るやつ
app-in:
	docker-compose exec app bash

# アプリコンテナをビルドし直すやつ
refresh-app:
	docker compose build --no-cache app

# app.logに起動ログを出力するやつ
# 例: app.logger.info(hoge) とかを関数内に書くとapp.logに出力されるよ
watch-flask-log:
	docker-compose exec app cat app.log

# uwsgi.logを拝見するやつ
watch-uwsgi-log:
	docker-compose exec app cat /var/log/uwsgi.log

# nginx.logを拝見するやつ
watch-nginx-log:
	docker logs -f flask_nginx