from flask.views import MethodView
from flask import Flask

class Foo(MethodView):
    def get(self, name):
        return name

    def post(self):
        return "post"

    def put(self, name):
        return "put"

    def delete(self, name):
        return "delete"

view_func = Foo.as_view("Foo")

app = Flask(__name__)

app.add_url_rule("/", "index", view_func=view_func, methods=["GET",])

app.add_url_rule("/", "index", view_func =view_func, methods=["POST",])
app.add_url_rule("/<int:user_id>",  view_func = view_func, methods=["GET", "PUT", "DELETE"])

app.run()
