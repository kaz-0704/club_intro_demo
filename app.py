from flask import Flask, render_template, request, redirect
from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import sessionmaker, scoped_session



app = Flask(__name__)
engine = create_engine('mysql+pymysql://{user}:{password}@{host}/{db_name}?charset=utf8'.format(**{
    'user': "mysql",
    'password': "mylocal37918",
    'host': "localhost",
    'db_name': "test_db"
}))
Base = declarative_base()



class User(Base):
    __tablename__ = 'users'
    name = Column('name', String(30), primary_key=True)
    password = Column('password', String(30))


class Club(Base):
    __tablename__ = 'clubs'
    name = Column('name', String(30), primary_key=True)
    belonging = Column('belonging', String(30))


class Post(Base):
    __tablename__ = 'posts'
    name = Column('name', String(30), primary_key=True)
    content = Column('cnotent', String(500))

 

Base.metadata.create_all(engine)  # 実際にデータベースを構築します
SessionMaker = sessionmaker(bind=engine)  # Pythonとデータベースの経路です
session = scoped_session(SessionMaker)  # 経路を実際に作成しました




@app.route("/", methods=["GET"])
def main():
    posts = session.query(Post).all()
    return render_template("main.html", cont=posts)



@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        users = session.query(User).all()
        return render_template("register.html", cont=users)
    
    else:
        name = request.form['name']
        password = request.form['pass']
        user = User(name='{}'.format(name), password='{}'.format(password))
        session.add(user)
        session.commit()
        return redirect("/register")



@app.route("/post", methods=["GET", "POST"])
def search():
    if request.method == "GET":
        return render_template("post.html")

    else:
        name = request.form['name']
        content = request.form['content']
        post = Post(name='{}'.format(name), content='{}'.format(content))
        session.add(post)
        session.commit()
        return redirect("/")


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8888, threaded=True)
    
