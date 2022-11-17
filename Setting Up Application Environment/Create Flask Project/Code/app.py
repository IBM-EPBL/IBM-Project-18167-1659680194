from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<h1>Hello, This is Sample Flask Application</h1>"

app.run()