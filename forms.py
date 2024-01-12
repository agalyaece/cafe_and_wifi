from wtforms import Form, StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo, URL


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


class AddCafe(Form):
    name = StringField("Cafe Name", validators=[DataRequired()])
    map_url = StringField("Cafe location URL", validators=[DataRequired(), URL()])
    img_url = StringField("Cafe Image URL", validators=[DataRequired(), URL()])
    location = StringField("Cafe location", validators=[DataRequired()])
    seats = StringField("Number of seats available", validators=[DataRequired()])
    has_toilet= StringField("has toilets", validators=[DataRequired()])
    has_sockets = StringField("has power sockets", validators=[DataRequired()])
    has_wifi = StringField("has wi-fi", validators=[DataRequired()])
    can_take_calls = StringField("can able to take calls", validators=[DataRequired()])
    coffee_price = StringField("coffee price", validators=[DataRequired()])
    submit = SubmitField("Add this cafe!")