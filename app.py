from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
import requests

from second import second
from api import api
#from session import session

app = Flask(__name__)

app.register_blueprint(second, url_prefix="")

app.register_blueprint(api, url_prefix="/api")

#app.register_blueprint(session, url_prefix="")

app.secret_key = 'hello'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(hours = 24)

db = SQLAlchemy(app)


@app.route('/flight', methods = ['POST', 'GET'])
def api():
    if request.method == 'GET':
        country = request.args.get('country')
        currency = request.args.get('currency')
        locale = request.args.get('locale')
        originplace = request.args.get('originplace')
        destinationplace = request.args.get('destinationplace')
        outboundpartialdate = request.args.get('outboundpartialdate')

        url = f"https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/browsequotes/v1.0/{country}/{currency}/{locale}/{originplace}/{destinationplace}/{outboundpartialdate}"
    
        querystring = {"inboundpartialdate":"2019-12-01"}
        
        headers = {
        'x-rapidapi-key': "089d02225bmshefa31c6ca5f2456p154c11jsnebd679e760b4",
        'x-rapidapi-host': "skyscanner-skyscanner-flight-search-v1.p.rapidapi.com"
        }

        departure_date =  str(requests.request("GET", url, headers=headers, params = querystring).json()['Quotes'][0]['OutboundLeg']['DepartureDate'])
        price = str(requests.request("GET", url, headers=headers, params = querystring).json()['Quotes'][0]['MinPrice'])
        return f'Hello the price is {price} and you leave the {departure_date}'
        #return str(requests.request("GET", url, headers=headers, params = querystring).json()['Quotes'][0]['MinPrice'])
      

 



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

@app.route('/user')
def user():
    if 'email' in session:
        email = session['email']
        return f'<h1>This is your email: {email} :)</h1>'
    else:
        return redirect(url_for('signin'))



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






