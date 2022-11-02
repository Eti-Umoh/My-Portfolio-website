from urllib import request
from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField
from wtforms.validators import DataRequired,Email

class EmailForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()])
    messages = TextAreaField('Message',validators=[DataRequired()])
    submit = SubmitField('Submit')