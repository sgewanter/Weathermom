from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=25)])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    zip_code = StringField('Zip Code', validators=[DataRequired()])
    phone_number = StringField('Phone Number', validators=[DataRequired()])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=25)])
    submit = SubmitField('Login')

class UserProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)], render_kw={"class": "form-control"})
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=25)], render_kw={"class": "form-control"})
    first_name = StringField('First Name', validators=[DataRequired()], render_kw={"class": "form-control"})
    last_name = StringField('Last Name', validators=[DataRequired()], render_kw={"class": "form-control"})
    city = StringField('City', validators=[DataRequired()], render_kw={"class": "form-control"})
    zip_code = StringField('Zip Code', validators=[DataRequired()], render_kw={"class": "form-control"})
    phone_number = StringField('Phone Number', validators=[DataRequired()], render_kw={"class": "form-control"})
    submit = SubmitField('Update', render_kw={"class": "btn btn-primary"})


class UpdateProfileForm(FlaskForm):
    username = StringField('Username', render_kw={"class": "form-control"})
    password = PasswordField('Password', render_kw={"class": "form-control"})
    first_name = StringField('First Name', render_kw={"class": "form-control"})
    last_name = StringField('Last Name', render_kw={"class": "form-control"})
    city = StringField('City', render_kw={"class": "form-control"})
    zip_code = StringField('Zip Code', render_kw={"class": "form-control"})
    phone_number = StringField('Phone Number', render_kw={"class": "form-control"})
    submit = SubmitField('Update', render_kw={"class": "btn btn-primary"})
