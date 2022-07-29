from flask import Flask, render_template, request, redirect
import datetime
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# データベースのURIの指定
db_uri = os.environ.get('DATABASE_URL') or 'postgresql://localhost/muscle'
db_uri_rename = db_uri.replace('postgres://', 'postgresql://')

app.config['SQLALCHEMY_DATABASE_URI'] = db_uri_rename
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# データベースのteamテーブルの定義
class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.String(200))

# データベースのmemberテーブルの定義
class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    teamid = db.Column(db.Integer)
    start_finish = db.Column(db.String(10), default='start')

# データベースのlogテーブルの定義
class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    teamid = db.Column(db.Integer)
    datetime = db.Column(db.DateTime)
    start_finish = db.Column(db.String(10))

# ルートページ(最初のページ)
@app.route('/')
def index():
    teams = Team.query.all()
    return render_template("index.html", teams = teams)

# 各グループの詳細ページ
@app.route('/detail/<int:id>')
def detail(id):
    teamdata = Team.query.get(id)
    members = Member.query.filter_by(teamid=id).all()
    members_number = len(members)
    logs = Log.query.filter_by(teamid=id).all()
    logs_reverse = list(reversed(logs))
    active_users = Member.query.filter_by(teamid=id).filter_by(start_finish='start').all()
    active_users_number = len(active_users)
    return render_template("detail.html", td=teamdata, ms=members, logs=logs_reverse, mn=members_number, active_users = active_users, aun = active_users_number)

# 名前の登録
@app.route('/join', methods=["post"])
def join():
    name = request.form["name"]
    teamid = request.form["teamid"]
    newMember = Member(name=name, teamid=teamid)
    db.session.add(newMember)
    db.session.commit()
    return redirect("/detail/"+str(teamid))

# ログの登録
@app.route('/log', methods=["post"])
def log():
    name = request.form["name"]
    teamid = request.form["teamid"]
    dt = datetime.datetime.now()
    MemberSearch = Member.query.filter_by(teamid=teamid).filter_by(name=name).first()
    if MemberSearch == None:
        newMember = Member(name=name, teamid=teamid) 
        db.session.add(newMember)
        newLog = Log(name=name, teamid=teamid, start_finish='start', datetime=dt)
        db.session.add(newLog)
    else:
        if MemberSearch.start_finish == 'finish':
            MemberSearch.start_finish = 'start'
            newLog = Log(name=name, teamid=teamid, start_finish='start', datetime=dt)
            db.session.add(newLog)
        else: 
            MemberSearch.start_finish = 'finish'
            newLog = Log(name=name, teamid=teamid, start_finish='finish', datetime=dt)
            db.session.add(newLog)
    db.session.commit()
    return redirect("/detail/"+str(teamid))

# ルートページ(最初のページ)
@app.route('/detail_sub')
def detail_sub():
    return render_template("detail_sub.html")


if __name__ == '__main__':
    app.run()