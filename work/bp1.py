from flask import Flask
from bp import simple_page

app = Flask(__name__)
app.register_blueprint(simple_page, url_prefix="/pages")
app.run(debug  = True)

