#-*- coding: utf-8 -*-
from flaskext.wtf import Form, required, PasswordField, \
        BooleanField, TextField, HiddenField, SubmitField, equal_to, ValidationError, SubmitInput
from flaskext.babel import gettext, lazy_gettext as _
from common import getDB

db = getDB("app")
class BaseForm(Form):
    number = TextField(_(u"基地编号"), validators=[
                            required(message=_(u"有木有"))
                                               ])    
    name = TextField(_(u"基地名字"), validators=[
                        required(message=_(u"必须的")), ])

    city = TextField(_(u"基地所在城市"))
    next = HiddenField()

    def validate_number(self,  field):
        """
        验证唯一性
        """
        print "--------validate_number", field.data
        res =  db.base.find_one({"no": field.data })
        if res is not None > 0:
            raise ValidationError,  gettext(u"这个可以不重复的，在该一该吧！")

    def validate_name(self, field):
        res =  db.base.find_one({"name": field.data })
        if res is not None:
            raise ValidationError,  gettext(u"这个可以不重复的，在该一该吧！")


    def asDict(self):
        """比较不好的做法，数据产生拷贝了
        """
        d = {}
        for attr in self.showAttributes:
            d[attr] = self[attr].data
        print d
        return d


class BaseUpdateForm(BaseForm):
    """属性的名字和数据库的key是一致的，
    如果有按钮总是submit, showAttribes 在html显示的属性
    """
    showAttributes = ["number", "name", "city"]
    button = SubmitField(_(u"更新"))
    submit = lambda this, **x: this.button(id="updateBtnOK", **x)
    # submit = SubmitField(_(u"更新"))
    myID = "frmUpdate"

    def __init__(self):
        # Form.__init__(self, id="frmUpdate")
        super(BaseUpdateForm, self).__init__()

    def validate_number(self,  field):
        """
        验证唯一性
        """
        res =  db.base.find_one({"no": field.data })
        if res is not None > 0:
            raise ValidationError,  gettext(u"这个可以不重复的，在该一该吧！")

    def validate_name(self, field):
        res =  db.base.find_one({"name": field.data })
        if res is not None:
            raise ValidationError,  gettext(u"这个可以不重复的，在该一该吧！")


class BaseAddForm(BaseForm):
    showAttributes = ["number", "name", "city"]
    button  = SubmitField(_(u"添加"))
    submit = lambda this, **x: this.button(id="addBtnOK", **x)
    myID = "frmAdd"
    def __init__(self):
        super(BaseAddForm, self).__init__(id ="frmAdd")

