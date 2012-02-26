#ss
#-*-coding:utf-8 -*-

from flask import Flask
from views import  loginView


app = Flask(__name__)
app.register_blueprint(loginView)


if __name__ == "__main__":
	app.run(debug=True)
	
