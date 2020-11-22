from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
import requests

#from signup_form import SignupForm
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


'''@app.route('/flight', methods = ['POST', 'GET'])
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
        #return str(requests.request("GET", url, headers=headers, params = querystring).json()['Quotes'][0]['MinPrice'])'''
      

 



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


#class flights(db.Model):





@app.route('/show_test')
def show_all():
    return render_template('show_all.html', users = users.query.all())

@app.route('/', methods = ['GET', 'POST'])
def index():
    '''if request.method == 'POST':
        if not request.form['firstname'] or not request.form['lastname'] or not request.form['email'] or not request.form['password'] or not request.form['passwordconfirm']:
            return redirect(url_for('signup'))
        else:
            user = users(request.form['password'], request.form['email'], request.form['lastname'], request.form['firstname'])
            db.session.add(user)
            db.session.commit()
            #flash(f'Welcome {user[0]}!')
            return redirect(url_for('show_all'))'''
    if 'firstname' in session:
        return render_template('index.html', navbarname = f"Hello {session['firstname']}")
    else:
        return render_template('index.html', navbarname = 'You need to sign in to purchase')



@app.route('/change_profile')
def change_profile():
    if 'firstname' in session:
        user = users.query.filter_by(firstname = session['firstname'], lastname = session['lastname']).first()
        firstname = user.firstname
        lastname = user.lastname
        email = user.email
        password = user.password
        return render_template('change_profile.html', firstname = firstname, lastname = lastname, email = email, password = password)
    else:
        redirect(url_for('signin'))


@app.route('/change_profile_processing', methods = ['POST'])
def change_profile_processing():
    if request.method == 'POST':
        if not request.form['firstname'] or not request.form['lastname'] or not request.form['email']:
            flash('All fields are required.')
            return render_template('change_profile.html')
        else:
            old_firstname = session['firstname']
            old_lastname = session['lastname']
            user = users.query.filter_by(firstname = old_firstname, lastname = old_lastname).first()
            user.email = request.form['email']
            user.firstname = request.form['firstname']
            user.lastname = request.form['lastname']
            db.session.commit()
            session['firstname'] = user.firstname
            session['lastname'] = user.lastname
            firstname = user.firstname
            lastname = user.lastname
            email = user.email
            flash('Changes done successfully')
            return render_template('change_profile.html', firstname = firstname, lastname = lastname, email = email)


@app.route('/trains', methods = ["GET", "POST"])
def trains():
    if 'firstname' in session:
        return render_template('trains.html', navbarname = f"Hello {session['firstname']}")
    else:
        return render_template('trains.html', navbarname = 'You need to sign in to purchase')




@app.route('/autobus', methods = ['GET', 'POST'])
def autobus():
    if 'firstname' in session:
        return render_template('autobus.html', navbarname = f"Hello {session['firstname']}")
    else:
        return render_template('autobus.html', navbarname = 'You need to sign in to purchase')



@app.route('/flight_result')
def flights():
    if 'firstname' in session:
        return render_template('flight_result.html', navbarname = f"Hello {session['firstname']}")
    else:
        return render_template('flight_result.html', navbarname = 'You need to sign in to purchase')



@app.route('/user')
def user():
    if 'firstname' in session and 'lastname' in session:
        firstname = session['firstname']
        lastname = session['lastname']
        return f'<h1>This is your firstname: {firstname} and your last name is: {lastname} :)</h1>'
    else:
        return redirect(url_for('signin'))



@app.route('/signin', methods = ['POST', 'GET'])
def signin():
    if request.method == 'POST':
        session.permanent = True
        email = request.form['email']
        password = request.form['password']
        user_session = users.query.filter_by(password=password).first()
        session['firstname'] = user_session.firstname
        session['lastname'] = user_session.lastname
        return redirect(url_for('user'))
    else:
        if 'firstname' in session:
            return redirect(url_for('user'))

        return render_template('signin.html')



@app.route('/signup', methods = ['GET', 'POST'])
def signup():

    if request.method == 'POST':
        if not request.form['firstname'] or not request.form['lastname'] or not request.form['email'] or not request.form['password'] or not request.form['passwordconfirm']:
            flash('All fields are required.')
            return render_template('signup.html')
        else:
            user = users(request.form['password'], request.form['email'], request.form['lastname'], request.form['firstname'])
            db.session.add(user)
            db.session.commit()
            #session['firstname'] = users(request.form['firstname'])
            #session['lastname'] = users(request.form['lastname'])
            #flash(f'Welcome {user[0]}!')
            return redirect(url_for('show_all'))
    if request.method == 'GET':
        return render_template('signup.html')



@app.route('/logout')
def logout():
    if 'email' in session:
        email = session['email']
        flash(f'You have been logged out successfully: {email}', 'info')
    session.pop('firstname', None)
    session.pop('lastname', None)
    return redirect(url_for('signin'))




@app.route('/api/processing', methods = ['GET', 'POST'])
def process_flights():
    origin_country = request.args.get('origin_country')
    origin_city = request.args.get('origin_city')
    origin_airport = request.args.get('origin_airport')
    date = request.args.get('date')
    time = request.args.get('time')
    destination_country = request.args.get('destination_country')
    destination_city = request.args.get('destination_city')
    destination_airport = request.args.get('destination_airport')
    name = request.args.get('name')
    carrier_id = request.args.get('carrier_id')
    price = request.args.get('price')
    symbol = request.args.get('symbol')
    user = users.query.filter_by(firstname='ok').first()
    lastname = session['lastname']
    return str(user._id) + lastname + origin_country + origin_city + origin_airport + date + time + destination_country + destination_city + destination_airport + name + carrier_id + price + symbol




if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)








