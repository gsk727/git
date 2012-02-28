#-*- coding:utf-8 -*-

from flask import render_template
from myApp import app
from flask import url_for

@app.route("/")
def main():
    return render_template("index.html")

