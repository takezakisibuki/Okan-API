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
`make rebuild`
