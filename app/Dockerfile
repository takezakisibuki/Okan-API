# python 3.9 をベースにDockerイメージを作成
FROM python:3.9

# 作業ディレクトリを指定
WORKDIR /var/www/app

RUN apt-get update \
    && apt-get install -y vim \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

COPY . .

# ライブラリインストール
RUN pip install -U pip \
    && pip install --no-cache-dir -r /var/www/app/config/requirements.txt
