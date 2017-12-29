from flask import Flask
from flask_restful import Resource, Api
from flask_httpauth import HTTPBasicAuth
from db import get_plant_data, get_forecast_data, get_crypto_data, get_spent_amount

application = Flask(__name__)
api = Api(application)
auth = HTTPBasicAuth()

users = {
    "test": "test"
}

@auth.get_password
def get_pw(username):
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
        amount = sum([i['amount'] for i in profit_data])
        spent = get_spent_amount()

        return {
            'profit': ((amount - spent) / spent) * 100 ,
            'current_amount': amount,
            'detail': get_crypto_data()
        }

api.add_resource(Home, "/")
api.add_resource(Coins, "/coins")


if __name__ == "__main__":
    application.run(debug=True)


