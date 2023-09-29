# Okan-API
チーム「負けNAIST」のOkan-APIです。

## 環境構築
環境構築について簡単に説明します！<br>
っていっても基本dockerでコンテナ立ち上げるだけにしてます，悪しからず。<br>

1. リポジトリをクローンします<br>
    `git clone https://github.com/kokochin/Okan-API.git`
2. クローンしたリポジトリ(ディレクトリ)に侵入します<br>
    `cd Okan-API`
3. コンテナをビルドします。<br>
    `make up`
4. Flaskが起動したか確認します。<br>
    ブラウザで`http://localhost:5001`にアクセス

## 変更の反映について
いわゆるコンパイルみたいな作業です。<br>
ローカルで編集した後，編集内容を反映させるために以下のコマンドを実行してください。<br>
`make rebuild`
