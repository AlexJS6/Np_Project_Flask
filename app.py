from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)
app.secret_key = 'hello'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(hours = 24)

db = SQLAlchemy(app)


class users(db.Model):
    _id = db.Column('id', db.Integer, primary_key = True)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))


    def __init__(self, password, email, lastname, firstname):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = password


@app.route('/show_test')
def show_all():
    return render_template('show_all.html', users = users.query.all())

@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        if not request.form['firstname'] or not request.form['lastname'] or not request.form['email'] or not request.form['password'] or not request.form['passwordconfirm']:
            return redirect(url_for('signup'))
        else:
            user = users(request.form['password'], request.form['email'], request.form['lastname'], request.form['firstname'])
            db.session.add(user)
            db.session.commit()
            #flash(f'Welcome {user[0]}!')
            return redirect(url_for('show_all'))
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