#-*- coding: utf-8 -*-

from flask import Flask
from views import groups
from views import magazine
from views import main

app = Flask(__name__)
app.config.from_object("cfg")

app.register_blueprint(magazine.magazine)
app.register_blueprint(main.main)
app.register_blueprint(groups.groups)

from werkzeug.wsgi import DispatcherMiddleware

back = Flask(__name__)

@back.route("/")
def index():
    return "back"

application = DispatcherMiddleware(app, {"/back":back})

if __name__ == "__main__":
    app.run(debug=True)

