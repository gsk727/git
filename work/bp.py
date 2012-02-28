from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
from flask import url_for

simple_page = Blueprint("simple_page", __name__, template_folder="templates")

@simple_page.route("/", defaults={"page": "index"})
@simple_page.route("/<page>")
def show(page):
    try:
        print url_for("simple_page.show")
        print url_for("simple_page.show")

        return "hello world"
        return render_template("pages/%s.html" % page)
    except TemplateNotFound:
        abort(404)

# simple_page.run()
