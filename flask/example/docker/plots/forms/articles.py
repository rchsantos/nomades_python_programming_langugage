from wtforms import Form, StringField, TextAreaField
from wtforms.validators import DataRequired

class AddArticle(Form):
  title = StringField("Title", validators=[DataRequired()])
  body = TextAreaField("Body", validators=[DataRequired()], render_kw={"rows": 5})
