import csv

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin,LoginManager,login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from forms import RegisterForm, LoginForm, AddCafe


app = Flask(__name__)
app.config["secret_key"] = "bxmnbjrlali394ujtkty569y0iklap"

Bootstrap5(app)


login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cafes.db"
db = SQLAlchemy()
db.init_app(app)


class Cafe(db.Model):
    __tablename__ = "cafe"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25))
    username = db.Column(db.String(25), unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))


with app.app_context():
    db.create_all()


@app.route("/")
def index():
    result = db.session.execute(db.select(Cafe))
    posts = result.scalars().all()
    return render_template("index.html", all_posts=posts)


@app.route("/add_cafe", methods=["GET", "POST"])
def add_cafe():
    form = AddCafe(request.form)
    if request.method == "POST" and form.validate():
        new_cafe = Cafe(
            name=request.form.get("name"),
            map_url=request.form.get("map_url"),
            img_url=request.form.get("img_url"),
            location=request.form.get("loc"),
            has_sockets=bool(request.form.get("sockets")),
            has_toilet=bool(request.form.get("toilet")),
            has_wifi=bool(request.form.get("wifi")),
            can_take_calls=bool(request.form.get("calls")),
            seats=request.form.get("seats"),
            coffee_price=request.form.get("coffee_price"),
        )
        return render_template("add_cafe.html",msg_sent=True)

    return render_template("add_cafe.html", form=form, current_user=current_user, msg_sent=False)


@app.route("/remove_cafe/<int:post_id>")
def remove_cafe(post_id):
    api_key = request.args.get("api-key")
    if api_key == "TopSecretAPIKey":
        delete_cafe = db.get_or_404(Cafe, post_id)
        if delete_cafe:
            db.session.delete(delete_cafe)
            db.session.commit()
            return render_template("index.html")
        else:
            return render_template("index.html")
    else:
        return render_template("index.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        form_data = request.form
        with open("suggestions_form.csv", "a", newline= "" ) as file:
            writer = csv.writer(file)
            writer.writerow([form_data["name"], form_data["email"], form_data["subject"], form_data["message"]])
            return render_template("contact.html", msg_sent=True)
    return render_template("contact.html", msg_sent=False)


@app.route("/sign_up", methods=["GET", "POST"])
def register():
    form = RegisterForm(request.form)
    if request.method == "POST" and form.validate():

        result = (db.session.execute(db.select(User).where(User.email == form.email.data)))
        user = result.scalar()

        if user:
            flash("User with same email already exists, please login to continue")
            return redirect(url_for('login'))

        hash_and_salted_password = generate_password_hash(form.password.data,
                                                          method="pbkdf2:sha256",
                                                          salt_length=8)

        new_user = User(
            name=form.name.data,
            username=form.username.data,
            email=form.email.data,
            password=hash_and_salted_password,

        )

        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return render_template("register.html", msg_sent=True)
    return render_template("register.html", form=form, current_user=current_user, msg_sent=False)


@app.route("/login")
def login():
    form = LoginForm(request.form)
    if form.validate and request.method == "POST":
        user = (db.session.execute(db.select(User).where(User.email == form.email.data))).scalar()
        if not user:
            flash("your email does not exists")
            return redirect(url_for("login"))
        elif not check_password_hash(user.password, password=form.password.data):
            flash("password doesn't match login again!")
            return redirect(url_for("login"))
        else:
            login_user(user)
            return redirect(url_for("index"))
    return render_template("login.html", form=form, current_user=current_user)


if __name__ == "__main__":
    app.run(debug=True)