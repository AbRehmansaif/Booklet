from flask import Flask, request, render_template, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.secret_key = "your_secret_key"

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# Create DB tables
with app.app_context():
    db.create_all()

@app.route("/", methods=["GET", "POST"])
def sign_in():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session["user_name"] = user.name
            return redirect(url_for("home"))
        else:
            flash("Invalid credentials", "error")
    return render_template("signIn.html")

@app.route('/signup', methods=['GET','POST'])
def sign_up():
    if request.method == 'POST':
        # safely grab form values
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        # check for missing values
        if not name or not email or not password:
            flash('All fields are required.', 'error')
            return render_template('signUp.html')

        # ensure user doesn’t already exist
        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'error')
            return render_template('signUp.html')

        # create & hash password
        hashed_pw = generate_password_hash(password)

        # create new user and commit
        new_user = User(name=name, email=email, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please sign in.', 'success')
        return redirect(url_for('sign_in'))

    # GET just renders the form
    return render_template('signUp.html')

@app.route("/home")
def home():
    if "user_name" in session:
        return render_template("home.html", username=session["user_name"])
    return redirect(url_for("sign_in"))

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("sign_in"))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)