from flask import Flask, render_template, request
import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/receive", methods=["post"])
def post():
    name = request.form["name"]
    detail = request.form["detail"]
    time = datetime.datetime.now()
    return render_template("receive.html", name = name, detail=detail, time=time)

if __name__ == '__main__':
    app.run(debug=True)