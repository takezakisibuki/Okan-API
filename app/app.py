from flask import Flask, redirect, url_for, render_template, request, jsonify
import psycopg2
import logging
from psycopg2.extras import DictCursor
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from datetime import datetime,date
from sqlalchemy.dialects import postgresql as pg
from sqlalchemy.schema import ForeignKey
import okan_gpt
import swagger
from flask_swagger_ui import get_swaggerui_blueprint
import random

# from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
logging.basicConfig(filename='app.log', level=logging.DEBUG)
logging.basicConfig(filename='app.log', level=logging.ERROR)

def pg_conn():
    setting = {
        'host': 'flask_db', # dbコンテナ名を指定
        'port': '5432',
        'dbname': 'postgres',
        'user': 'postgres',
        'password': 'postgres'
    }
    return psycopg2.connect(**setting)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@flask_db:5432/postgres'
engine = create_engine(f'postgresql://postgres:postgres@flask_db:5432/postgres', echo=True)
db = SQLAlchemy(app)
# app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_host=1, x_port=1, x_proto=1)

class users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    flag=db.Column(pg.ARRAY(db.Integer, dimensions=1), nullable=False)

class diary(db.Model):
    __tablename__ = 'diary'

    id = db.Column(db.Integer, primary_key=True)
    content=db.Column(db.Text,nullable=False)
    comment=db.Column(db.Text,nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    user_id=db.Column(db.Integer,db.ForeignKey("users.id", name="fk_test_results_00",onupdate='CASCADE', ondelete='CASCADE'),nullable=False)

class Post(db.Model):
    __tablename__ = 'persons'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    detail = db.Column(db.Text)
    due = db.Column(db.DateTime, nullable=False)

class Post2(db.Model):
    __tablename__ = 'persons2'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    detail = db.Column(db.String(100))
    due = db.Column(db.DateTime, nullable=False)

@app.route('/', methods=['GET', 'POST'])
def index():    
    if request.method == 'GET':
        posts = Post.query.order_by(Post.due).all()
        return render_template('index.html', posts=posts,today=date.today())

    else:
        # 日記内容と日付を取得
        title = request.form.get('title')
        due = request.form.get('due')
        due = datetime.strptime(due, '%Y-%m-%d')

        # 日記内容をOpenAIに投げて、おかんコメントを取得
        res = okan_gpt.create( title )

        # 日記内容・おかんコメント・日付をDBに保存
        new_post = Post(title=title, detail=res["choices"][0]["message"]["content"], due=due)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/') # 変更

@app.route('/create',methods=['POST'])
def create():
    user_post=users(id=1,flag=[0 for _ in range(25)])
    db.session.add(user_post)
    db.session.commit()
    new_post = diary(id=1,content='ありがとう', comment='おおきに',time= datetime.now(),user_id=1)
    db.session.add(new_post)
    db.session.commit()
    return 'DBに保存しました'

'''-----------------以下は本機能のAPI-----------------'''



'''-----------------以下はテスト用のAPI-----------------'''
# ① 日記を投稿するAPI パラメータ：user-id,diary-content
@app.route('/api/test/okan-api',methods=['POST'])
def okan_api():
    params = request.form
    if 'user-id' in params and 'diary-content' in params:
        test = {
            "comment": '"'+params.get('diary-content')+'"に対するおかんからのテストコメントやでぇ',
        }
    else:
        test = {
            "error": "user-idかdiary-contentが指定されていません",
        }
    return jsonify(test)

# ② 日記を取得するAPI パラメータ：diary-id
@app.route('/api/test/diary',methods=['GET'])
def diary_api():
    # URLパラメータ
    params = request.args
    if 'diary-id' in params:
        if 'diary-id' == 1:
            test = {
                'id':params.get('diary-id'),
                'content': "あんたの日記内容やでぇ",
                'comment': "おかんからのテストコメントやでぇ",
                'time': '2023-10-1',
            }
        elif 'diary-id' == 2:
            test = {
                'id':params.get('diary-id'),
                'content': "あんたの日記内容やでぇ.2",
                'comment': "おかんからのテストコメントやでぇ.2",
                'time': '2023-10-2',
            }
        else:
            test = {
                'id':params.get('diary-id'),
                'content': "None",
                'comment': "この日記は存在せーへんでぇ",
                'time': '1970-1-1',
            }
    else: 
        test = {
            "error": "idが指定されていません",
        }
    return jsonify(test)

# ③ 指定月の日記一覧を取得するAPI パラメータ：user-id,month
@app.route('/api/test/monthly',methods=['GET'])
def monthly_api():
    # URLパラメータ
    params = request.args
    if 'user-id' in params and 'month' in params:
        if 'month' == 10:
            test = {
                "diary_list": [
                    { "id": 1, "date": 2023-10-1 },
                    { "id": 2, "date": 2023-10-2 },
                ]
            }
        else:
            test = {
                "diary_list": []
            }
    else:
        test = {
            "error": "user-idかmonthが指定されていません",
        }
    return jsonify(test)

# ④ ギフトガチャを回すAPI パラメータ：user-id
@app.route('/api/test/gift-rand',methods=['POST'])
def rand_api():
    # URLパラメータ
    params = request.form
    if 'user-id' in params:
        test = {
            "gift_number": random.randrange(25),
        }
    else:
        test = {
            "error": "user-idが指定されていません",
        }
    return jsonify(test)

# ⑤ ギフトフラグを取得するAPI パラメータ：user-id
@app.route('/api/test/gift-flag',methods=['GET'])
def gift_flag_api():
    # URLパラメータ
    params = request.args
    if 'user-id' in params:
        test = {
            "gift_flag": [0 for _ in range(25)],
        }
    else:
        test = {
            "error": "user-idが指定されていません",
        }
    return jsonify(test)


'''-----------------以下はswaggerの記述-----------------'''
SWAGGER_URL = '/api/docs'
API_URL = '/swagger'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "おかんAPI"
    },
)
app.register_blueprint(swaggerui_blueprint)

@app.route('/swagger')
def swagger_rule():
    json = swagger.swag()
    return (json)


# @app.route('/',methods=['GET'])
# def get_text():
#     posts=diary.query

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     # hoge = 'fuga'
#     # app.logger.info(hoge)
#     if request.method == 'GET':
#         posts = Post.query.order_by(Post.due).all()
#         return render_template('index.html', posts=posts,today=date.today())

#     else:
#         title = request.form.get('title')
#         detail = request.form.get('detail')
#         due = request.form.get('due')
        
#         due = datetime.strptime(due, '%Y-%m-%d')#文字列をdatetimeに変換
#         new_post = Post(title=title, detail=detail, due=due)

#         db.session.add(new_post)
#         db.session.commit()
#         return redirect('/') # 変更

# @app.route('/create')
# def create():
#     return render_template('create.html')

# @app.route('/detail/<int:id>')
# def read(id):
#     post = Post.query.get(id)

#     return render_template('detail.html', post=post)

# @app.route('/delete/<int:id>')
# def delete(id):
#     post = Post.query.get(id)

#     db.session.delete(post)
#     db.session.commit()
#     return redirect('/')

# @app.route('/update/<int:id>', methods=['GET', 'POST'])
# def update(id):
#     post = Post.query.get(id)
#     if request.method == 'GET':
#         return render_template('update.html', post=post)
#     else:
#         post.title = request.form.get('title')
#         post.detail = request.form.get('detail')
#         post.due = datetime.strptime(request.form.get('due'), '%Y-%m-%d')

#         db.session.commit()
#         return redirect('/')

# @app.route('/result',methods=["GET"])
# def result():
#     # posts=Post.query.limit(10).all()
#     # sql_statement = (
#     #                     select([
#     #                         User.id,
#     #                         User.name, 
#     #                         User.age
#     #                     ]).filter(
#     #                         (User.name == user_name) &
#     #                         (User.age >= user_age) 
#     #                     ).limit(10)
#     #                 )
#     sql_statement = 'SELECT * FROM persons limit 10'
    
#     df = pd.read_sql_query(sql=sql_statement, con=engine)

#     return render_template('dbresult.html',table=(df.to_html(classes="mystyle")))
#     # return render_template('dbresult.html',table=posts)

if __name__ == "__main__":
    app.run(debug=True)
