from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'hello'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(hours = 24)


db = SQLAlchemy(app)

class users(db.Model):
    _id = db.Column('id', db.Integer, primary_key = True)
    password = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __init__(self, password, email):
        self.password = password
        self.email = email

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/flights')
def flights():
    return render_template('flights.html')

@app.route('/signin', methods = ['POST', 'GET'])
def signin():
    if request.method == 'POST':
        session.permanent = True
        email = request.form['email']
        password = request.form['password']
        session['email'] = email
        return redirect(url_for('user'))
    else:
        if 'email' in session:
            return redirect(url_for('user'))

        return render_template('signin.html')

@app.route('/user')
def user():
    if 'email' in session:
        email = session['email']
        return f'<h1>This is your email: {email} :)</h1>'
    else:
        return redirect(url_for('signin'))


@app.route('/signup')
def signup():
        return render_template('signup.html')

@app.route('/logout')
def logout():
    if 'email' in session:
        email = session['email']
        flash(f'You have been logged out successfully: {email}', 'info')
    session.pop('email', None)
    return redirect(url_for('signin'))

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)