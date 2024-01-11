from wtforms import Form, StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo


# create from to register new user
class RegisterForm(Form):
    name = StringField("Name", validators=[Length(min=3, max=25), DataRequired(message="Please fill this field!")])
    username = StringField("UserName", validators=[Length(min=3,max=25), DataRequired(message="Please fill this field!")])
    email = StringField("email", validators=[Email(message="Please enter a valid email address"), DataRequired(message="Please fill this field!")])
    password = PasswordField("Password", validators=[Length(min=3,max=25),EqualTo(fieldname="confirm", message="Your password do not match") ,DataRequired(message="Please fill this field!")])
    confirm = PasswordField("Confirm Password", validators=[Length(min=3,max=25), DataRequired(message="Please fill this field!")])
    submit = SubmitField("submit!")


class LoginForm(Form):
    email = StringField("email", validators=[Length(min=8, max=50),Email(message="Please enter a valid email address"),
                                             DataRequired(message="Please fill this field!")])
    password = PasswordField("Password", validators=[Length(min=3, max=25),

                                                     DataRequired(message="Please fill this field!")])