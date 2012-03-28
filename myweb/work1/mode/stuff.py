#-*- coding: utf-8 -*-
import re
from mode import Mode

stuffMap = [
            ("email", u"电子邮件"),
            ("name", u"名字"),
            ("begin", u"入职时间"),
            ("end", u"离职时间"),
            ("role", u"职位"),
            ("des", u"描述", ),
            ("base", u"基地"),
            ("password", u"密码"),
            ("status", u"状态"),
]


class StuffMode(Mode):
    _cName = "user"
    attributes = stuffMap
    database = "app"
    keys=("email", )

    def __init__(self):
        super(StuffMode, self).__init__()


    def compileQuery(self):
        """
        virtual 
        """
        email = self.doc["email"]  # :)
        p = re.compile(email, re.IGNORECASE)
        return {"email": p}
        
 
