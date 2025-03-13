from flask import Flask, jsonify, render_template
import data

app = Flask(__name__)

SQLITE_URI = 'sqlite:///data/flights.sqlite3'
IATA_LENGTH = 3

# Create an instance of the Data Object using our SQLite URI
data_manager = data.FlightData(SQLITE_URI)

@app.route('/', methods=['GET'])
def index():
    api_info = {
        "message": "Welcome to the Flight API!",
        "endpoints": {
            "/flight/<int:flight_id>": "GET flight details by ID",
            "/delayed_flights/airline/<string:airline>": "GET delayed flights by airline",
            "/delayed_flights/airport/<string:airport>": "GET delayed flights by origin airport",
            "/flights/date/<int:year>/<int:month>/<int:day>": "GET flights by date"
        }
    }
    endpoint_example = {
        "/flight/<int:flight_id>": "/flight/281",
        "/delayed_flights/airline/<string:airline>": "/delayed_flights/airline/United%20Air%20Lines%20Inc.",
        "/delayed_flights/airport/<string:airport>": "/delayed_flights/airport/JFK",
        "/flights/date/<int:year>/<int:month>/<int:day>": "/flights/date/2015/1/3"
    }
    return render_template('index.html', api_info=api_info, endpoint_example=endpoint_example)

@app.route('/flight/<int:flight_id>', methods=['GET'])
def get_flight_by_id(flight_id):
    result = data_manager.get_flight_by_id(flight_id)
    return jsonify([row._asdict() for row in result])


@app.route('/delayed_flights/airline/<string:airline>', methods=['GET'])
def get_delayed_flights_by_airline(airline):
    result = data_manager.get_delayed_flights_by_airline(airline)
    return jsonify([row._asdict() for row in result])


@app.route('/delayed_flights/airport/<string:airport>', methods=['GET'])
def get_delayed_flights_by_airport(airport):
    result = data_manager.get_delayed_flights_by_airport(airport)
    return jsonify([row._asdict() for row in result])


@app.route('/flights/date/<int:year>/<int:month>/<int:day>', methods=['GET'])
def get_flights_by_date(year, month, day):
    result = data_manager.get_flights_by_date(day, month, year)
    return jsonify([row._asdict() for row in result])

def main():
    app.run(debug=True)

if __name__ == '__main__':
    main()