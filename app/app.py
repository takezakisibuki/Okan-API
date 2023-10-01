from flask import Flask, redirect, url_for, render_template, request
import psycopg2
import logging
from psycopg2.extras import DictCursor
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from datetime import datetime,date
from sqlalchemy.dialects import postgresql as pg
from sqlalchemy.schema import ForeignKey


# from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
logging.basicConfig(filename='app.log', level=logging.DEBUG)

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

# class diary(db.Model):
#     __tablename__ = 'diary'

#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(30), nullable=False)
#     detail = db.Column(db.String(100))
#     due = db.Column(db.DateTime, nullable=False)

@app.get('/')
def index():
    return render_template('index.html')

# @app.route('/get',methods=['GET'])
# def get_text():
#     posts=diary.query

@app.route('/create',methods=['POST'])
def create():
    user_post=users(id=1,flag=[0 for _ in range(25)])
    db.session.add(user_post)
    db.session.commit()
    new_post = diary(id=1,content='ありがとう', comment='おおきに',time= datetime.now(),user_id=1)
    db.session.add(new_post)
    db.session.commit()
    return 'DBに保存しました'


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
