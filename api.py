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
        price = str(requests.request("GET", url, headers=headers, params = querystring).json()['Quotes'][0]['MinPrice'])
        return f'Hello the price is {price} and you leave the {departure_date}'
        #return str(requests.request("GET", url, headers=headers, params = querystring).json()['Quotes'][0]['MinPrice'])
       