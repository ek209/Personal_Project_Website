from flask_wtf import FlaskForm
from wtforms import StringField, FileField, SelectField, SubmitField, IntegerField, PasswordField
from wtforms.validators import DataRequired, Length
from flask_ckeditor import CKEditorField

class MorseForm(FlaskForm):
    """Creates form fields and buttons for morse code translating.

    Args:
        FlaskForm (FlaskForm): Inherits FlaskForm for base of form.
    """
    english = CKEditorField("English", validators=[Length(max=1000)])
    morse = CKEditorField("Morse", validators=[Length(max=1000)])
    convert_morse = SubmitField('Convert to Morse')
    convert_english = SubmitField('Convert to English')

class TypingSpeedTestForm(FlaskForm):
    text = CKEditorField("Type Here: ")
    start = SubmitField("Start")
    stop = SubmitField("Stop")

class WatermarkForm(FlaskForm):
    """Creates the form for Image Watermarker

    Args:
        FlaskForm (FlaskForm): Inherits FlaskForm for base of form.
    """
    watermark_text = StringField('Text', validators=[Length(max=1000)])
    img_to_mark = FileField('Image', validators=[DataRequired()])
    font_size = IntegerField('Font size', validators=[DataRequired()])
    font_name = SelectField('Font', choices=['Dejavu Sans Mono'], validators=[DataRequired()])
    add_space = SelectField('Add space at end?', choices=['Yes', 'No'], validators=[DataRequired()])
    submit = SubmitField('Watermark')