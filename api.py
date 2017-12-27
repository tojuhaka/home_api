from flask import Flask
from flask_restful import Resource, Api
from db import get_plant_data, get_forecast_data

application = Flask(__name__)
api = Api(application)


class Plants(Resource):
    def get(self):
        result = {}
        result['forecast'] = get_forecast_data()
        result['plants'] = get_plant_data()
        return result

api.add_resource(Plants, "/")


if __name__ == "__main__":
    application.run(debug=True)


