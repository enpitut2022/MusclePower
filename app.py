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

# ルートページ(最初のページ)
@app.route('/')
def index():
    teams = Team.query.all()
    return render_template("index.html", teams = teams)

# 各グループの詳細ページ
@app.route('/detail/<int:id>')
def detail(id):
    teamdata = Team.query.get(id)
    members = Member.query.filter_by(teamid=id)
    return render_template("detail.html", td=teamdata, ms=members)

# 名前の登録
@app.route('/join', methods=["post"])
def join():
    name = request.form["name"]
    teamid = request.form["teamid"]
    newMember = Member(name=name, teamid=teamid)
    db.session.add(newMember)
    db.session.commit()
    return redirect("/detail/"+str(teamid))

if __name__ == '__main__':
    app.run()