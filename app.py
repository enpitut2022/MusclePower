from flask import Flask, render_template, request
import datetime
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://dorkfibkuvlyob:1db04b410515df5d6a68a6fb88ba5272d7e5c7f5951442b1997441b0b5ef2ab5@ec2-34-235-31-124.compute-1.amazonaws.com:5432/d8b4bie8clcibc'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.String(200))

@app.route('/')
def index():
    teams = Team.query.all()
    return render_template("index.html", teams = teams)

@app.route('/detail/<int:id>')
def detail(id):
    teamdata = Team.query.get(id)
    return render_template("detail.html", td=teamdata)

"""
不必要になったコード(念の為残しておく)
@app.route('/walking')
def walking():
    return render_template("walking.html")

@app.route('/sixpad')
def sixpad():
    return render_template("sixpad.html")

@app.route('/squat')
def squat():
    return render_template("squat.html")

@app.route("/receive", methods=["post"])
def post():
    name = request.form["name"]
    detail = request.form["detail"]
    time = datetime.datetime.now()
    return render_template("receive.html", name = name, detail=detail, time=time)
"""

if __name__ == '__main__':
    app.run()