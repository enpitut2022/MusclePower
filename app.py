from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return '走れ三日坊主'

if __name__ == '__main__':
    app.run()