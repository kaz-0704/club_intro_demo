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
    id = Column('id', String(30), primary_key=True)
    password = Column('pass', String(30))
    name = Column('name', String(30))
    belonging = Column('belonging', String(30))
    area = Column('area', String(30))
    category = Column('category', String(30))


class Post(Base):
    __tablename__ = 'posts'
    name = Column('name', String(30), primary_key=True)
    content = Column('cnotent', String(500))
    

 

Base.metadata.create_all(engine)  # 実際にデータベースを構築します
SessionMaker = sessionmaker(bind=engine)  # Pythonとデータベースの経路です
session = scoped_session(SessionMaker)  # 経路を実際に作成しました



check = False
access_club = None

@app.route("/", methods=["GET", "POST"])
def main():
    global check
    if request.method == "GET":
        posts = session.query(Post).all()
        return render_template("main.html", cont=posts, check=check)


@app.route("/login", methods=["GET", "POST"])
def login():
    global check
    if request.method == "GET":
        return render_template("login.html", check=check)
    
    else:
        id = request.form['id']
        password = request.form['pass']
        club = session.query(Club).filter(Club.id=='{}'.format(id))
        for c in club:  club_pass = c.password
        if club_pass == password:
            check = True
            global access_club
            access_club = c
            return render_template("login.html", check=check)
        else:
            return render_template("login.html", check=check)



@app.route("/user_register", methods=["GET", "POST"])
def user_register():
    if request.method == "GET":
        users = session.query(User).all()
        return render_template("user_register.html", cont=users)
    
    else:
        name = request.form['name']
        password = request.form['pass']
        user = User(name='{}'.format(name), password='{}'.format(password))
        session.add(user)
        session.commit()
        return redirect("/user_register")



@app.route("/club_register", methods=["GET", "POST"])
def club_register():
    if request.method == "GET":
        clubs = session.query(Club).all()
        return render_template("club_register.html", cont=clubs)
    
    else:
        id = request.form['id']
        password = request.form['pass']
        name = request.form['name']
        belonging = request.form['belonging']
        area = request.form['area']
        category = request.form['category']
        club = Club(id='{}'.format(id), password='{}'.format(password), name='{}'.format(name), belonging='{}'.format(belonging), area='{}'.format(area), category='{}'.format(category))
        session.add(club)
        session.commit()
        return redirect("/club_register")



@app.route("/clubpage", methods=["GET", "POST"])
def clubpage():
    return render_template("clubpage.html", club=access_club)



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
    
