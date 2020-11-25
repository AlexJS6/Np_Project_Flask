from flask import Flask, redirect, url_for, render_template, request, session, flash, Blueprint
import requests

api = Blueprint('api', __name__, static_folder="static", template_folder="templates")


@api.route('/flight', methods = ['POST', 'GET'])
def flight_api():
    if request.method == 'GET':
        country = request.args.get('country')
        currency = request.args.get('currency')
        locale = request.args.get('locale')
        originplace = request.args.get('originplace')
        destinationplace = request.args.get('destinationplace')
        outboundpartialdate = request.args.get('outboundpartialdate')
        
        if country is None or currency is None or locale is None or originplace is None or destinationplace is None or outboundpartialdate is None:
            flash('All fields are required!', 'success')
            redirect(url_for('index'))
        else:
            url = f"https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/browsequotes/v1.0/{country}/{currency}/{locale}/{originplace}/{destinationplace}/{outboundpartialdate}"
        
            querystring = {"inboundpartialdate":"2019-12-01"}
            
            headers = {
            'x-rapidapi-key': "089d02225bmshefa31c6ca5f2456p154c11jsnebd679e760b4",
            'x-rapidapi-host': "skyscanner-skyscanner-flight-search-v1.p.rapidapi.com"
            }

            departure_date =  str(requests.request("GET", url, headers=headers, params = querystring).json()['Quotes'][0]['OutboundLeg']['DepartureDate'][:10])
            departure_time = str(requests.request("GET", url, headers=headers, params = querystring).json()['Quotes'][0]['QuoteDateTime'][-8:])
            price = str(requests.request("GET", url, headers=headers, params = querystring).json()['Quotes'][0]['MinPrice'])
            carrier_id = str(requests.request("GET", url, headers=headers, params = querystring).json()['Carriers'][0]['CarrierId'])
            name = str(requests.request("GET", url, headers=headers, params = querystring).json()['Carriers'][0]['Name'])
            symbol = str(requests.request("GET", url, headers=headers, params = querystring).json()['Currencies'][0]['Symbol'])
            origin_city = str(requests.request("GET", url, headers=headers, params = querystring).json()['Places'][0]['CityName'])
            origin_country = str(requests.request("GET", url, headers=headers, params = querystring).json()['Places'][0]['CountryName'])
            origin_airport = str(requests.request("GET", url, headers=headers, params = querystring).json()['Places'][0]['Name'])
            destination_city = str(requests.request("GET", url, headers=headers, params = querystring).json()['Places'][1]['CityName'])
            destination_country = str(requests.request("GET", url, headers=headers, params = querystring).json()['Places'][1]['CountryName'])
            destination_airport = str(requests.request("GET", url, headers=headers, params = querystring).json()['Places'][1]['Name'])
            direct = str(requests.request("GET", url, headers=headers, params = querystring).json()['Quotes'][0]['Direct'])

            #return f'<h1>Hello the price is {price} and you leave the {departure_date}</h1>'
            #return str(requests.request("GET", url, headers=headers, params = querystring).json()['Quotes'][0]['MinPrice'])'''
            #return requests.request('GET', url, headers = headers, params = querystring).json()
            #return f'<div style="background-color: red"><p>{departure_date}</br>{departure_time}</br>{price}</br>{carrier_id}</br>{name}</br>{symbol}</br>{origin_country}</br>{origin_city}</br>{origin_airport}</br>{destination_country}</br>{destination_city}</br>{destination_airport}</br>{direct}</p></div>'
            return render_template('flight_result.html', date = departure_date, time = departure_time, price = price, carrier_id = carrier_id, name = name, symbol = symbol, origin_country = origin_country, origin_city = origin_city, origin_airport = origin_airport, destination_country = destination_country, destination_city = destination_city, destination_airport = destination_airport, navbarname = f"Hello {session['firstname']}")




    @api.route('/car', methods = ['POST', 'GET'])
    def car_api():
        if request.method == 'GET':
            pickup_location = request.args.get('pickup_location')
            pickup_date = request.args.get('pickup_date') + 'T' + request.args.get('pickup_time')
            
            return_location = request.args.get('return_location')
            return_date = request.args.get('return_date') + 'T' + request.args.get('return_time')
            

            url = f"https://priceline-com.p.rapidapi.com/cars/{str(pickup_location)}"

            querystring = {"return_date":str(return_date),"pickup_date":str(pickup_date),"return_location_id":str(return_location)}

            headers = {
                'x-rapidapi-key': "089d02225bmshefa31c6ca5f2456p154c11jsnebd679e760b4",
                'x-rapidapi-host': "priceline-com.p.rapidapi.com"
                }

            #return return_location
            return requests.request('GET', url, headers = headers, params = querystring).json()

            #response = requests.request("GET", url, headers=headers, params=querystring)

            #print(response.text)
        
        