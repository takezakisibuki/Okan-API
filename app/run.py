from flask import Flask, redirect, url_for, render_template
import psycopg2 
from psycopg2.extras import DictCursor
# from werkzeug.middleware.proxy_fix import ProxyFix


app = Flask(__name__)
# app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_host=1, x_port=1, x_proto=1)

def pg_conn():
    setting = {
        'host': 'flask_db', # dbコンテナ名を指定
        'port': '5432',
        'dbname': 'postgres',
        'user': 'postgres',
        'password': 'postgres'
    }
    return psycopg2.connect(**setting)

@app.get('/')
def index():
    return render_template('index.html')

@app.get('/red')
def red():
    with pg_conn() as conn:
        with conn.cursor(cursor_factory=DictCursor) as cur:
            sql = "INSERT INTO users(name) values('jessy')"
            cur.execute(sql)
            conn.commit()
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run()