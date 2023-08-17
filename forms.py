from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, PasswordField
from wtforms.validators import DataRequired, URL, Email, Length
from flask_ckeditor import CKEditorField

class MorseForm(FlaskForm):
    english = CKEditorField("English", validators=[Length(max=1000)])
    morse = CKEditorField("Morse", validators=[Length(max=1000)])
    convert_morse = SubmitField('Convert to Morse')
    convert_english = SubmitField('Convert to English')