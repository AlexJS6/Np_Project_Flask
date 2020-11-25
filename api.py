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
            flash('All fields are required!', 'error')
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



@api.route('/hotel', methods = ['GET', 'POST'])
def hotel_api():
    if request.method == 'GET':
        check_in = request.args.get('check_in')
        check_out = request.args.get('check_out')
        latitude = request.args.get('latitude')
        longitude = request.args.get('longitude')
        locale = request.args.get('locale')
        rooms = request.args.get('rooms')
        currency = request.args.get('currency')
        
        if check_in is None or check_out is None or latitude is None or longitude is None or locale is None or rooms is None or currency is None:
            flash('All fields are required!', 'error')
            redirect(url_for('hotels'))
        else:

            url = "https://hotels-com-free.p.rapidapi.com/srle/listing/v1/brands/hotels.com"

            querystring = {"checkIn": str(check_in),"checkOut": str(check_out),"lat": str(latitude),"lon": str(longitude),"locale": str(locale),"rooms": str(rooms),"currency": str(currency)}

            headers = {
                'x-rapidapi-key': "089d02225bmshefa31c6ca5f2456p154c11jsnebd679e760b4",
                'x-rapidapi-host': "hotels-com-free.p.rapidapi.com"
                }

            #return requests.request('GET', url, headers = headers, params = querystring).json()

            #response = requests.request("GET", url, headers=headers, params=querystring)
            
            response = requests.request("GET", url, headers=headers, params=querystring).json()

            #name = response['data']['body']['searchResults']['results'][0]['name']
            #price = response['data']['body']['searchResults']['results'][0]['ratePlan']['price']['current']
            #country = response['data']['body']['searchResults']['results'][0]['address']['countryName']
            #locality = response['data']['body']['searchResults']['results'][0]['address']['locality']
            #street = response['data']['body']['searchResults']['results'][0]['address']['streetAddress']
            #rating = str(float(response['data']['body']['searchResults']['results'][0]['guestReviews']['rating'])*2)
            return response['data']['body']['searchResults']['results'][0]
            return render_template('hotel_result.html', name = name, price = price, country = country, locality = locality, street = street, rating = rating, navbarname = f"Hello {session['firstname']}")