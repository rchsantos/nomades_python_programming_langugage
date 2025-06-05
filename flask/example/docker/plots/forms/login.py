from wtforms import Form, StringField, IntegerField, FileField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegisterForm(Form):
  firstname = StringField("Firstname WTF", validators=[DataRequired(), Length(min=3)])
  lastname = StringField("Lastname WTF", validators=[DataRequired(), Length(min=3)])
  email = EmailField("Email WTF", validators=[DataRequired(), Email()])
  uid = StringField("Username WTF", validators=[DataRequired(), Length(min=3, max=10)])
  age = IntegerField("Age WTF", validators=[DataRequired()])
  pp = FileField("Profile picture WTF")
  pwd = PasswordField("Password WTF", validators=[DataRequired()])
  pwd2 = PasswordField("Repeat password WTF", validators=[DataRequired(), EqualTo("pwd", message="Password mismatch")])
