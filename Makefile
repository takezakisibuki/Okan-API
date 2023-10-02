# Docker を立ち上げるやつ
up:
	docker compose up -d

# app.py いじった後にコンパイルするやつ
run:
	docker-compose rm -fsv app
	docker compose up -d
#	docker compose exec app pip install flask_sqlalchemy

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
log-flask:
	docker-compose exec app cat app.log

# uwsgi.logを拝見するやつ
log-uwsgi:
	docker-compose exec app cat /var/log/uwsgi.log

# nginx.logを拝見するやつ
log-nginx:
	docker logs -f flask_nginx

# テストAPIを実行
test-api:
	curl -X POST 'http://localhost:8080/api/test/okan-api?user-id=1&diary-content=hoge'
	curl -X GET 'http://localhost:8080/api/test/diary?diary-id=1'
	curl -X GET 'http://localhost:8080/api/test/monthly?user-id=1&month=10'
	curl -X POST 'http://localhost:8080/api/test/gift-rand?user-id=1'
	curl -X GET 'http://localhost:8080/api/test/gift-flag?user-id=1'