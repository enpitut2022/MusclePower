from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/receive", methods=["post"])
def post():
    text = request.form["name"]
    return render_template("receive.html", name = text)

if __name__ == '__main__':
    app.run(debug=True)