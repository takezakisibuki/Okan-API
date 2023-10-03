from flask import Flask, redirect, url_for, render_template, request, jsonify
import psycopg2
import logging
from psycopg2.extras import DictCursor
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text
from datetime import datetime,date
from sqlalchemy.dialects import postgresql as pg
from sqlalchemy.schema import ForeignKey
import okan_gpt
import swagger
from flask_swagger_ui import get_swaggerui_blueprint
import random

# 最初の最初のおまじない（Flask）
app = Flask(__name__)

# ログの出力を許可するためのおまじない（./app.logに出力されます）
logging.basicConfig(filename='app.log', level=logging.DEBUG)
logging.basicConfig(filename='app.log', level=logging.ERROR)

# DB接続用のこーんを設定するおまじない
def pg_conn():
    setting = {
        'host': 'flask_db', # dbコンテナ名を指定
        'port': '5432',
        'dbname': 'postgres',
        'user': 'postgres',
        'password': 'postgres'
    }
    return psycopg2.connect(**setting)

# PostgreSQLにSQLAlchemyを紐づけるためのおまじない
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@flask_db:5432/postgres'
engine = create_engine(f'postgresql://postgres:postgres@flask_db:5432/postgres', echo=True)
db = SQLAlchemy(app)

# ユーザテーブル
class users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    flag=db.Column(pg.ARRAY(db.Integer, dimensions=1), nullable=False)

# 日記テーブル
class diary(db.Model):
    __tablename__ = 'diary'

    id = db.Column(db.Integer, primary_key=True)
    content=db.Column(db.Text,nullable=False)
    comment=db.Column(db.Text,nullable=False)
    time = db.Column(db.Date, nullable=False)
    user_id=db.Column(db.Integer,db.ForeignKey("users.id", name="fk_test_results_00",onupdate='CASCADE', ondelete='CASCADE'),nullable=False)

# テスト用のテーブル（擬似フロントエンドから使用）
class Post(db.Model):
    __tablename__ = 'persons'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    detail = db.Column(db.Text)
    due = db.Column(db.DateTime, nullable=False)


'''-----------------以下は本機能のAPI-----------------'''

# ② 日記を取得するAPI パラメータ：diary-id
@app.route('/api/diary',methods=['GET'])
def get_diary():
    diary_id=request.args.get('diary-id')
    posts=diary.query.filter(diary.id==diary_id).all()
    # app.logger.info(type(posts))
    for post in posts:
        diary_json={
            "id": post.id,
            "内容": post.content,
            "コメント": post.comment,
            "日付": post.time.strftime('%Y-%m-%d'),
        }
    app.logger.info(diary_json)
    return jsonify(diary_json)

# ③ 日記を取得するAPI パラメータ：diary-id
@app.route('/api/monthly',methods=['GET'])
def month_info():
    user_id=request.args.get('user-id')
    month=request.args.get('month', type=int)
    # monthの入ったテーブルを作成
    # select *,to_char(time,'MM') AS month
    # from diary;
    # usersテーブルと結合し、month=10のものをピックアップ
    with engine.connect() as conn:
        posts=conn.execute(text("SELECT * \
                            FROM (\
                            SELECT *,to_char(time,'MM')AS month\
                            FROM diary\
                            )AS diary2\
                            JOIN users\
                            ON diary2.user_id=users.id\
                            WHERE(users.id=user_id and diary2.month=month)\
                            "))
    hoge=[]
    for post in posts:
        hoge.append({
            "日記ID": post.id,
            "日付": post.time
        })
    return jsonify(hoge)


'''-----------------以下はテスト用のAPI-----------------'''
# 【テスト】① 日記を投稿するAPI パラメータ：user-id,diary-content
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

# 【テスト】② 日記を取得するAPI パラメータ：diary-id
@app.route('/api/test/diary',methods=['GET'])
def diary_api():
    # URLパラメータ
    params = request.args
    if 'diary-id' in params:
        if params.get('diary-id',type=int) == 1:
            test = {
                'id':params.get('diary-id'),
                'content': "あんたの日記内容やでぇ",
                'comment': "おかんからのテストコメントやでぇ",
                'time': '2023-10-1',
            }
        elif params.get('diary-id',type=int) == 2:
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

# 【テスト】③ 指定月の日記一覧を取得するAPI パラメータ：user-id,month
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

# 【テスト】④ ギフトガチャを回すAPI パラメータ：user-id
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

# 【テスト】⑤ ギフトフラグを取得するAPI パラメータ：user-id
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

# 【テスト】日記テーブルにテストレコードを作成する
@app.route('/test-table',methods=['POST'])
def test_table():
    user_post=users(id=1,flag=[0 for _ in range(25)])
    db.session.add(user_post)
    db.session.commit()
    new_post = diary(id=1,content='ありがとう', comment='おおきに',time= datetime.now(),user_id=1)
    db.session.add(new_post)
    db.session.commit()
    return 'DBに保存しました'


'''-----------------以下はswaggerの記述-----------------'''
# swagger そのもののルーティング
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

# swagger の設定ファイル
@app.route('/swagger')
def swagger_rule():
    json = swagger.swag()
    return (json)


'''-----------------以下はテストページの記述(後で消す)-----------------'''
# おかん日記風のフロントエンドのモックです
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

@app.route('/create')
def create():
    return render_template('create.html')

@app.route('/detail/<int:id>')
def read(id):
    post = Post.query.get(id)
    return render_template('detail.html', post=post)

@app.route('/delete/<int:id>')
def delete(id):
    post = Post.query.get(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/')

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    post = Post.query.get(id)
    if request.method == 'GET':
        return render_template('update.html', post=post)
    else:
        post.title = request.form.get('title')
        post.detail = request.form.get('detail')
        post.due = datetime.strptime(request.form.get('due'), '%Y-%m-%d')
        db.session.commit()
        return redirect('/')

@app.route('/result',methods=["GET"])
def result():
    sql_statement = 'SELECT * FROM persons limit 10'
    df = pd.read_sql_query(sql=sql_statement, con=engine)
    return render_template('dbresult.html',table=(df.to_html(classes="mystyle")))


if __name__ == "__main__":
    app.run(debug=True)
