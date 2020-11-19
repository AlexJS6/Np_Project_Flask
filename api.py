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

        url = f"https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/browsequotes/v1.0/{country}/{currency}/{locale}/{originplace}/{destinationplace}/{outboundpartialdate}"
    
        querystring = {"inboundpartialdate":"2019-12-01"}
        
        headers = {
        'x-rapidapi-key': "089d02225bmshefa31c6ca5f2456p154c11jsnebd679e760b4",
        'x-rapidapi-host': "skyscanner-skyscanner-flight-search-v1.p.rapidapi.com"
        }

        departure_date =  str(requests.request("GET", url, headers=headers, params = querystring).json()['Quotes'][0]['OutboundLeg']['DepartureDate'])
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
        return f'<div style="background-color: red"><p>This is the best flight:</p><h2>price: {price} and leaves: {departure_time}, good trip</h2></div>'