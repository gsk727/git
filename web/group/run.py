#-*-coding: utf-8 -*-
from myApp import app

import groups
import magazine
import main
import publish
import j


def run():
    app.run(host = app.config.get("HOST"), port =  app.config.get("PORT"), debug=True)

if __name__ == "__main__":
    run()
