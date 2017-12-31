import json
from flask import Flask
from flask_restful import Resource, Api
from flask_httpauth import HTTPBasicAuth
from db import get_plant_data, get_forecast_data, get_crypto_data, get_coin_spent_amount, get_seligson_data, get_seligson_spent_amount

application = Flask(__name__)
api = Api(application)
auth = HTTPBasicAuth()

@auth.get_password
def get_pw(username):
    users = {}
    with open('/home/pi/users.json') as f:
        users = json.load(f)

    if username in users:
        return users.get(username)
    return None

class Home(Resource):
    def get(self):
        result = {}
        result['forecast'] = get_forecast_data()
        result['plants'] = get_plant_data()
        return result


class Coins(Resource):

    @auth.login_required
    def get(self):
        profit_data = get_crypto_data()
        seligson_data = get_seligson_data()

        coin_amount = sum([i['amount'] for i in profit_data])
        seligson_amount = sum(i['amount'] for i in seligson_data)

        coin_spent = get_coin_spent_amount()
        seligson_spent = get_seligson_spent_amount()

        coins = {
            'profit': ((coin_amount - coin_spent) / coin_spent) * 100 ,
            'current_amount': coin_amount,
            'details': profit_data
        }

        seligson = {
            'profit': ((seligson_amount - seligson_spent) / seligson_spent) * 100 ,
            'current_amount': seligson_amount,
            'details': seligson_data
        }

        return {
            'seligson': seligson,
            'coins': coins
        }

    def options(self):
        result = {}
        return result

@application.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', 'null')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET')
    return response


api.add_resource(Home, "/")
api.add_resource(Coins, "/coins")



if __name__ == "__main__":
    application.run(debug=True)


