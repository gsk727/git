#-*-coding: utf-8 -*-
from myApp import app

import j
from views import groups, main, magazine


def run():
    app.register_blueprint(groups.groups)
    app.register_blueprint(main.main)
    app.register_blueprint(magazine.magazine)
    app.run(host = app.config.get("HOST"), port =  app.config.get("PORT"), debug=True, threaded = True) #threaded = true

if __name__ == "__main__":
    run()
