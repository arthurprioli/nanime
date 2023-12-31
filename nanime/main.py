from flask import Flask, render_template, request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user
from models import anime


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"

app.config["SECRET_KEY"] = "NANIME"

db = SQLAlchemy()

login_manager = LoginManager()
login_manager.init_app(app)

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)


db.init_app(app)

with app.app_context():
    db.create_all()

@login_manager.user_loader
def loader_user(user_id):
    return Users.query.get(user_id)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/animes")
def animes():
    return render_template("lista_animes.html")

@app.route("/search_anime/<anime_name>", methods=["GET", "POST"])
def search_anime(anime_name):
    anime.search_anime(anime_name)
    return render_template("home.html", anime_name=anime_name)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user = Users(username=request.form.get("username"),
                     password=request.form.get("password"))
        try:
            db.session.add(user)
            db.session.commit()
        except:
            print(f"Erro no registro do usuário {user.username} no banco de dados")
        return redirect(url_for("login"))
    return render_template("sign_up.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = Users.query.filter_by(username=request.form.get("username")).first()

        if user and (user.password == request.form.get("password")):
            login_user(user)
            return redirect(url_for("home"))
        else:
            flash("Usuário ou senha incorretos.", 'error')
            return redirect(url_for("login"))
    return render_template("login.html")

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)