from flask_wtf import FlaskForm
from wtforms import StringField, FileField, SelectField, SubmitField, IntegerField, PasswordField
from wtforms.validators import DataRequired, URL, Email, Length
from flask_ckeditor import CKEditorField

class MorseForm(FlaskForm):
    english = CKEditorField("English", validators=[Length(max=1000)])
    morse = CKEditorField("Morse", validators=[Length(max=1000)])
    convert_morse = SubmitField('Convert to Morse')
    convert_english = SubmitField('Convert to English')

class WatermarkForm(FlaskForm):
    watermark_text = StringField('Text', validators=[Length(max=1000)])
    img_to_mark = FileField('Image', validators=[DataRequired()])
    font_size = IntegerField('Font size', validators=[DataRequired()])
    font_name = SelectField('Font', choices=['Dejavu Sans Mono'],)
    add_space = SelectField('Add space at end?', choices=['Yes', 'No'])
    submit = SubmitField('Watermark')