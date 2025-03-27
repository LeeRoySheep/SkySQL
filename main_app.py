import data
from datetime import datetime
import sqlalchemy
from flask import Flask, jsonify, request

SQLITE_URI = 'sqlite:///data/flights.sqlite3'
IATA_LENGTH = 3

app = Flask(__name__)

data_manager = data.FlightData(SQLITE_URI)

@app.route('/', methods=['GET'])
def get_data():
    flight_id = request.args.get('id', "").lower()
    date = request.args.get('date', "").lower()
    airport = request.args.get('airport', "").lower()
    airline = request.args.get('airline', "").lower()
    all_airlines = request.args.get('all_airlines', "").lower()
    delays_by_hour = request.args.get('hourly_delays', "").lower()
    delays_by_route = request.args.get('delays_routes', "").lower()
    delays_by_route_location = request.args.get('routes_with_location', "").lower()
    try:
        if flight_id:
            results = data_manager.get_flight_by_id(int(flight_id))
            results = [dict(result._mapping) for result in results]
            return jsonify(results), 200
        elif date:
            date = datetime.strptime(date, '%d/%m/%Y')
            results = data_manager.get_flight_by_date(date.day,date.month,date.year)
            results = [dict(result._mapping) for result in results]
            return jsonify(results), 200
        elif airport:
            if airport.isalpha() and len(airport) == IATA_LENGTH:
                results = data_manager.get_delayed_flights_by_airport(airport)
                results = [dict(result._mapping) for result in results]
                return jsonify(results), 200
            else:
                return jsonify("error","Bad Request for airport!"), 401
        elif airline:
            results = data_manager.get_delayed_flights_by_airline(airline)
            results = [dict(result._mapping) for result in results]
            return jsonify(results), 200
        elif all_airlines:
            if all_airlines.upper() == "True".upper():
                results = data_manager.get_delayed_flights_by_airlines()
                results = [dict(result._mapping) for result in results]
                return jsonify(results), 200
            else:
                return jsonify("error","Bad request for delays by airline!"), 401
        elif delays_by_hour:
            if delays_by_hour.upper() == "True".upper():
                results = data_manager.get_delayed_flights_by_hours()
                results = [dict(result._mapping) for result in results]
                return jsonify(results), 200
            else:
                return jsonify("error", "Bad request for delays by hour!"), 401
        elif delays_by_route:
            if delays_by_route.upper() == "True".upper():
                results = data_manager.get_delayed_routes()
                results = [dict(result._mapping) for result in results]
                return jsonify(results), 200
            else:
                return jsonify("error", "Bad request for delays by route!"), 401
        elif delays_by_route_location:
            if delays_by_route_location.upper() == "True".upper():
                results = data_manager.get_delayed_routes_with_lon_lat()
                results = [dict(result._mapping) for result in results]
                return jsonify(results), 200
            else:
                return jsonify("error", "Bad request for delays by route with location!"), 401
        else:
            return jsonify("error", "Bad request no parameters given!"), 401
    except Exception as e:
        return jsonify("error", f"Bad request: {e}"), 401


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5002, debug=True)