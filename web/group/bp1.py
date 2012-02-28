from flask import Flask
from bp import simple_page

app = Flask(__name__)
app.register_blueprint(simple_page)
app.run(debug  = True)


