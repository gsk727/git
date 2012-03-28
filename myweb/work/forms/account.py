#-*- coding: utf-8 -*-

from flaskext.wtf import Form, required, PasswordField, \
        BooleanField, TextField, HiddenField, SubmitField

#from flaskext.babel import gettext, lazy_gettext as _

class LoginForm(Form):
    username = TextField(u"电子邮件", validators=[
                        required(message=u"必须的"), ])
 
    password = PasswordField(u"密码")
    remember = BooleanField(u"记住密码")

    next = HiddenField()
    submit = SubmitField("登录")

