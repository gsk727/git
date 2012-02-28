from werkzeug.contrib.cache import MemcachedCache
from memcache import Client
import sys

cache = Client(["127.0.0.1:12000"], debug=True)

print sys.argv
#cache.set("foo", "sss")
if sys.argv[1] == "1":
    cache.set("foo", "asdsadasdsadas",  4, 1)

else:
    print cache.get("foo")
#


