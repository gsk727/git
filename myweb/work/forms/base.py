#-*- coding: utf-8 -*-
from flaskext.wtf import Form, required, PasswordField, \
        BooleanField, TextField, HiddenField, SubmitField, equal_to
from flaskext.babel import gettext, lazy_gettext as _

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
        if len(res) > 0:
            raise ValidationError,  gettext("这个可以不重复的，在该一该吧！")

    def validate_name(self, field):
        res =  db.base.find_one({"name": field.data })
        if len(res) > 0:
            raise ValidationError,  gettext("这个可以不重复的，在该一该吧！")

class BaseUpdateForm(BaseForm):
    """属性的名字和数据库的key是一致的，
    如果有按钮总是submit, showAttribes 在html显示的属性
    """
    showAttributes = ["number", "name", "city"]
    submit = SubmitField(_(u"提交更新"))


class BaseAddForm(BaseForm):
    showAttributes = ["number", "name", "city"]
    submit = SubmitField(_(u"添加"))