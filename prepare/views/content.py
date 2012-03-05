#-*- coding: utf-8 -*-

from basebp import BaseAppBP

class ContentBP(BaseAppBP):
    __name = "content"
    __url_prefix = "/content"
    def __init__(self):
        super(ContentBP, self).__init__( 
                    ContentBP.__name, 
                    __name__, 
                    url_prefix = ContentBP.__url_prefix, debug = True)


ContentView = ContentBP()

@ContentView.route("/content/<int:cid>")
def content_get(cid):
    return  "pass"
