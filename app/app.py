from flask import Flask, redirect, url_for, render_template, request, jsonify,abort,Response
import psycopg2
import logging
from psycopg2.extras import DictCursor
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text
from datetime import datetime,date,timedelta
from sqlalchemy.dialects import postgresql as pg
from sqlalchemy.schema import ForeignKey
import okan_gpt
import swagger
from sqlalchemy.orm import sessionmaker
from flask_swagger_ui import get_swaggerui_blueprint
import random
import pytz
import copy
import jwt
import functools
import bcrypt
import json
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


'''-----------------以下はデータベースモデル-----------------'''
# ユーザテーブル
class users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    flag=db.Column(pg.ARRAY(db.Integer, dimensions=1), nullable=False)
    pas=db.Column(db.String(255),nullable=False)
    account=db.Column(db.String(255),nullable=False,unique=True)
    name=db.Column(db.String(255),nullable=True)


# 日記テーブル
class diary(db.Model):
    __tablename__ = 'diary'

    id = db.Column(db.Integer, primary_key=True)
    content=db.Column(db.Text,nullable=False)
    comment=db.Column(db.Text,nullable=False)
    time = db.Column(db.Date(), nullable=False)
    user_id=db.Column(db.Integer,db.ForeignKey("users.id", name="fk_test_results_00",onupdate='CASCADE', ondelete='CASCADE'),nullable=False)

'''-----------------以下は認証周りのAPI・メソッド-----------------'''

# ログイン認証用関数
def login_required(method):
    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        header = request.headers.get('Authorization')
        # token = header.split()
        token=header
        try:
            decoded = jwt.decode(token,'SECRET_KEY',algorithms='HS256')
            user_id=decoded['id']
    
        except jwt.DecodeError:
            return jsonify({"error":"Token is not valid."}),400
            # return "Token is not valid."
        except jwt.ExpiredSignatureError:
            return jsonify({"error":"Token is expired"}),400
            # return "Token is expired."
        return method(user_id,*args, **kwargs)
    return wrapper


# A. [POST] id と password をもらってアクセストークンを発行するAPI
@app.route('/api/authorize',methods=['POST'])
def authorize():
    # passwordとidをクエリパラメータとして取得
    # クエリパラメータでもrequest.form.getで取得。argsだと取って来れない。
    input_id = request.form.get('id',type=int)
    input_password = request.form.get('password')
    user_pass = db.session.query(users.pas).filter(users.id==input_id).first()
    #idがテーブルに登録されていなければエラーを返す
    if user_pass is None:
        return jsonify({"error":f"Your id is not registered: input id is {input_id}"}),400
    # パスワードが間違っていればエラーを返す
    app.logger.info(bcrypt.__version__)
    if not bcrypt.checkpw(input_password.encode('utf-8'), user_pass[0].encode('utf-8')):
        return jsonify({"error":f"Your password is wrong: input password is {input_password}"}),400
    # トークンを時間とidから生成
    exp = datetime.utcnow() + timedelta(days=7)
    encoded = jwt.encode({'id': input_id,'exp': exp}, 'SECRET_KEY', algorithm='HS256')
    response = {'user_id':input_id,'token':encoded}
    return jsonify(response)

# B. [POST] テーブルをマイグレートしてユーザを新規登録するAPI
@app.route('/api/registration', methods=['POST'])
def register_user():
    db.create_all()
    Account = request.form.get('account')
    password = request.form.get('password')
    app.logger.info(Account)
    app.logger.info(password)
    if not Account or not password:
        # return jsonify({"error": "アカウントとパスワードを提供してください"}),400
        return jsonify({"error": "plese enetner pas and account"}),400
    existing_user = users.query.filter_by(account=Account).first()
    # app.logger.info("ここにはきています")
    if existing_user:
        # return jsonify({"error": "ユーザーは既に登録されています"}),400
        return jsonify({"error": "alleady exist"}),400
    # パスワードをハッシュ化して保存
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    password_hash = password_hash.decode('utf8')
    app.logger.info(password_hash)
    new_user = users(flag=[0 for _ in range(20)],pas=password_hash,account=Account)
    # app.logger.info("ここにはきています")
    db.session.add(new_user)
    db.session.commit()

    # 登録したDBからPasとidを取得
    record=users.query.filter(users.account==Account).first()
    user_id=record.id
    user_pas=record.pas

    # トークンを時間とidから生成
    exp = datetime.utcnow() + timedelta(days=7)
    encoded = jwt.encode({'id': user_id,'exp': exp}, 'SECRET_KEY', algorithm='HS256')

    # tokenとIDを返す
    res={
        "id":user_id,
        "token":encoded
    }
    return Response(response=json.dumps(res,ensure_ascii=False,indent=4), status=400)
    


'''-----------------以下は本機能のAPI-----------------'''
# ① [POST] 日記保存とオカンコメントの生成＆格納API
@app.route('/api/okan-api',methods=['POST'])
@login_required
def okan_api(login_required_userID):
    # ユーザIDと日記内容のフォームパラメータをゲット
    params = request.form
    # 今日の日付を日本時間で取得
    today=datetime.now(pytz.timezone('Asia/Tokyo'))
    date_today = today.date()
    user_id=params.get('user-id',type=int)
    # db内にすでに今日日記が書かれてあるかの確認
    posts=db.session.query(diary).filter(diary.user_id==user_id,diary.time==date_today).all()
    # 書かれてないなら日記の内容とその他の情報をdiaryに保存
    user = db.session.query(users).filter(users.id == user_id).first()
    if not user:
        return jsonify({"error": "指定されたユーザIDは存在しません"}),400
    if len(posts)==0:
        # パラメータが正しければ保存
        if 'user-id' in params and 'diary-content' in params:
            content=params.get('diary-content')
            comment=okan_gpt.create(content)
            new_record=diary(content=content,comment=comment["choices"][0]["message"]["content"],time=date_today,user_id=user_id)
            db.session.add(new_record)
            db.session.commit()
            # idは一回レコード作成しないと生成されないのでもう一回取りに行く
            diary_dates=db.session.query(diary).filter(diary.user_id==user_id,diary.time==date_today)
            app.logger.info(diary_dates)
            for diary_date in diary_dates:
                test={
                    "id":diary_date.id,
                    "content":diary_date.content,
                    "comment":diary_date.comment,
                    "date":diary_date.time.strftime('%Y-%m-%d'),
                    "user_id":diary_date.user_id,
                }
            res=Response(response=json.dumps(test,ensure_ascii=False,indent=4), status=200)
        # 正しくなければエラーを返す
        else:
            test = {
                "error": "user-idかdiary-contentが指定されていません",
            }
            res=Response(response=json.dumps(test,ensure_ascii=False,indent=4), status=400)
    # 書かれているならエラーを返す
    else :
        test={"error":"今日の日記はもう書いたよ"}
        res=Response(response=json.dumps(test,ensure_ascii=False,indent=4), status=400)
    return res

# ② 日記を取得するAPI パラメータ：diary-id
@app.route('/api/diary',methods=['GET'])
@login_required
def get_diary(login_required_userID):
    diary_id=request.args.get('diary-id')
    app.logger.info('diary-id:')
    app.logger.info(diary_id)
    # diary_id をクエリパラメータからゲットできていれば
    if not diary_id is None:
        posts=diary.query.filter(diary.id==diary_id).all()
        # 入力されたIDの日記が見つかれば内容を返す。
        if len(posts)!=0:
            for post in posts:
                diary_json={
                    "id": post.id,
                    "content": post.content,
                    "comment": post.comment,
                    "date": post.time.strftime('%Y-%m-%d'),
                }
            res =Response(response=json.dumps(diary_json,ensure_ascii=False,indent=4), status=200)

        else:
            diary_json={
            "error": "Not find a diary for this ID"
            }
            res =Response(response=json.dumps(diary_json,ensure_ascii=False,indent=4), status=400)

    else:
        diary_json={
            "error": "Please input diary_id"
        }
        res =Response(response=json.dumps(diary_json,ensure_ascii=False,indent=4), status=400)
    return res
   

# ③ 日記を取得するAPI パラメータ：diary-id
@app.route('/api/monthly',methods=['GET'])
@login_required
def month_info(login_required_userID):
    user_id=request.args.get('user-id')
    #ここにそもそもuser_idを識別するid文がないのが問題
    if not user_id is None:
        month=request.args.get('month')
        year=request.args.get('year')
        if not (month is None) or (year is None):
            ym=str(year+"-"+month)
            # ym(year-month)の入ったテーブルを作成
            # SELECT *,to_char(time,'YYYY-MM') AS ym
            # FROM diary;
            # usersテーブルと結合し、diary2.ym=ymのものをピックアップ
            with engine.connect() as conn:
                sql_query = text("SELECT diary2.id, diary2.time \
                  FROM ( \
                    SELECT *, to_char(time, 'YYYY-MM') AS ym \
                    FROM diary \
                  ) AS diary2 \
                  JOIN users ON diary2.user_id = users.id \
                  WHERE users.id = :user_id AND diary2.ym = :ym")
                params = {"user_id": user_id, "ym": ym}
                posts = conn.execute(sql_query,params)
            year_month_diary=[]
            for post in posts:
                year_month_diary.append({
                    "id": post.id,
                    "date": post.time.strftime('%Y-%m-%d'),
                })
            res =Response(response=json.dumps(year_month_diary,ensure_ascii=False,indent=4), status=200)
        else:
            year_month_diary={
                "error":"Year or Month have not been entered"
            }
            res =Response(response=json.dumps(year_month_diary,ensure_ascii=False,indent=4), status=400)
    else:
        year_month_diary={
            "error":"Please input a user-id"
        }
        res =Response(response=json.dumps(year_month_diary,ensure_ascii=False,indent=4), status=400)
    return res
    

# ④ ギフトガチャを回すAPI パラメータ：user-id
@app.route('/api/gift-rand', methods=['POST'])
@login_required
def rand_api_j(login_required_userID):
    # URLパラメータ
    params = request.form
    if 'user-id' in params:
        user_id = int(params['user-id'])
        ran = random.randint(0, 20)

        # ユーザーの存在を確認
        user = users.query.filter(users.id == user_id).first()
        if user:
            flag_list = copy.copy(user.flag)
            if flag_list is not None and 0 <= ran < len(flag_list):
                flag_list[ran] = 1 
                user.flag = flag_list
                app.logger.info(user.flag)
                app.logger.info(flag_list)
                db.session.commit()
                app.logger.info(type(user.id))
                app.logger.info(type(user.flag))
                app.logger.info(type(ran))
                data = {
                    "user_id":user.id,
                    "flag":user.flag,
                    "gift_number": ran
                    }
                res =Response(response=json.dumps(data,ensure_ascii=False,indent=4), status=200)
                
            else:
                data = {
                    "error": "指定されたユーザーが存在しないか、flag_listが正しく設定されていません",
                }
                res =Response(response=json.dumps(data,ensure_ascii=False,indent=4), status=400)
        else:
            data = {
                "error": "指定されたユーザーが存在しません",
            }
            res =Response(response=json.dumps(data,ensure_ascii=False), status=400)
    else:
        data = {
            "error": "user-idが指定されていません",
        }
        res =Response(response=json.dumps(data,ensure_ascii=False), status=400)
    return res
    

# ⑤ ギフトフラグを取得するAPI パラメータ：user-id
@app.route('/api/gift-flag',methods=['GET'])
@login_required
def gift_flag_api_j(login_required_userID):
    # URLパラメータ
    params = request.args
    if 'user-id' in params:
        user_id = int(params['user-id'])
        user = users.query.filter(users.id == user_id).first()
        if not user:
            return jsonify({"error": "指定されたユーザIDは存在しません"}),400
        flag_list = copy.copy(user.flag)
        if flag_list is not None :
            test = {
                "gift_flag": flag_list,
                "user_id":user_id
            }
            res =Response(response=json.dumps(test,ensure_ascii=False), status=200)
        else:
                test = {
                    "error": "指定されたユーザーが存在しないか、flag_listが正しく設定されていません",
                }
                res =Response(response=json.dumps(test,ensure_ascii=False), status=400)
    else:
        test = {
            "error": "user-idが指定されていません",
        }
        res =Response(response=json.dumps(test,ensure_ascii=False), status=400)
    return res

'''-----------------以下はテーブルを操作するデベロッパ向けAPI-----------------'''
# diaryレコードの一行を削除する関数
@app.route("/api/delete_diary", methods=["DELETE"])
def deleteDiary():
    try:
        diary_id_str = request.form.get('diary-id')
        app.logger.info(diary_id_str)
        if diary_id_str is None:
            return jsonify({'error': '日記IDパラメータが不足しています'}),400

        diary_id = int(diary_id_str)
        app.logger.info(diary_id)

        # diaryテーブルからエントリを取得
        diary_entry = db.session.query(diary).filter_by(id=diary_id).first()
        
        app.logger.info(diary_entry)

        if diary_entry:
            db.session.delete(diary_entry)
            db.session.commit()
            return jsonify({'message': '日記エントリが正常に削除されました'}),200
        else:
            return jsonify({'error': '日記エントリが見つかりません'}),400

    except ValueError:
        return jsonify({'error': '無効な日記IDです'}),400

# 【テスト】日記テーブルにテストレコードを作成する
@app.route('/test-table',methods=['POST'])
def test_table():
    user_post=users(id=1,flag=[0 for _ in range(20)])
    db.session.add(user_post)
    db.session.commit()
    new_post = diary(id=1,content='ありがとう', comment='おおきに',time= datetime.now(pytz.timezone('Asia/Tokyo')),user_id=1)
    db.session.add(new_post)
    db.session.commit()
    return 'DBに保存しました'

#  usersにパスワードと初期のギフトフラグを与えるAPI
@app.route('/test/user-date',methods=['POST'])
def test_user():
    arg=request.form.get("password")
    app.logger.info(arg)
    user_post=users(flag=[0 for _ in range(20)],pas=arg)
    db.session.add(user_post)
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

# webサーバが立ち上がっているか確認するようのルーティング
@app.route('/', methods=['GET', 'POST'])
def index():    
    return ('<h1>webサーバは正常に起動しています.</h1>')

if __name__ == "__main__":
    app.run(debug=True)
