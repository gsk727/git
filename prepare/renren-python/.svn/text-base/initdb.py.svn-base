import pymongo

host = "127.0.0.1"
port = 27017

db_name = "MyGame"
db = pymongo.Connection("127.0.0.1", port)[db_name]
db.user.update({"username":"game"}, {"username":"game", "password":"game", "life":100, "money":100}, True)

