# Okan-API
チーム「負けNAIST」のOkan-APIです。

## 環境構築
環境構築について簡単に説明します！<br>
っていっても基本dockerでコンテナ立ち上げるだけにしてます，悪しからず。<br>

1. リポジトリをクローンします<br>
    `git clone https://github.com/kokochin/Okan-API.git`
2. クローンしたリポジトリ(ディレクトリ)に侵入します<br>
    `cd Okan-API`
3. `.env.example`ファイルをコピーして名前を`.env`に変更します。
4. コンテナをビルドします。<br>
    `make up`
5. Flaskが起動したか確認します。<br>
    ブラウザで`http://localhost:8080`にアクセス<br>
    しぶきくんの作ったTodoアプリが見れたらOKです！
6. migrateを行います<br>
    `make app-in`<br>
    `python`で対話シェルに入る<br>
    migrate.py に記述しているコードを一行ずつ対話形式で実行
7. DBにテーブルが作成されたかを確かめます。
    `make db-in`<br>
    `psql -h flask_db -U postgres -d postgres`<br>
    あとはSQL文で中身を確かめてくださいな

## 変更の反映について
いわゆるコンパイルみたいな作業です。<br>
ローカルで編集した後，編集内容を反映させるために以下のコマンドを実行してください。<br>
`make run`


## ログファイルの閲覧について
**ログは合計3種類あります！**
### 1. nginx のログ
**コマンド**：`make log-nginx`<br>
500番台のエラーが返ってきたらまずここを見るといいです。
### 2. flask のログ
**コマンド**：`make log-flask`<br>
コマンド用意してますが、/app/app.log ファイルをVScodeから直接見てもらったらOKです。<br>
### 3. uwsgi のログ
**コマンド**：`make log-uwsgi`<br>
パッケージ足りないとか、そういう系のエラーはここにでます。<br>
ちなみにuwsgiはnginx(webコンテナ)とflask(appコンテナ)の架け橋です。（あまりにもざっくり）

## フロントエンド組の追加作業
`docker-compose.yml`の中の<br>
    ```
    ports:
      - "8080:80"
      # - "0.0.0.0:80:80"
    ```
を<br>
    ```
    ports:
      # - "8080:80"
    　- "0.0.0.0:80:80"
    ```
に変えてください。<br>

## APIの仕様書について
### バックエンド組はこう
`http://localhost:8080/api/docs`

### フロントエンド組はこう
`http://0.0.0.0/api/docs`