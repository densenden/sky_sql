#  /\\   /\\  --  /\\
# /  \\ /--\\  | /--\\
# \\__/ \\  /  | \\__/


from sqlalchemy import create_engine, text

# SQL queries
QUERY_FLIGHT_BY_ID = """
SELECT flights.*, airlines.airline, flights.ID as FLIGHT_ID, flights.DEPARTURE_DELAY as DELAY 
FROM flights 
JOIN airlines ON flights.airline = airlines.id 
WHERE flights.ID = :id
"""

QUERY_DELAYED_FLIGHTS_BY_AIRLINE = """
SELECT flights.*, airlines.airline, flights.ID as FLIGHT_ID, flights.DEPARTURE_DELAY as DELAY 
FROM flights 
JOIN airlines ON flights.airline = airlines.id 
WHERE airlines.airline = :airline AND flights.DEPARTURE_DELAY >= 20
"""

QUERY_DELAYED_FLIGHTS_BY_AIRPORT = """
SELECT flights.*, airlines.airline, flights.ID as FLIGHT_ID, flights.DEPARTURE_DELAY as DELAY 
FROM flights 
JOIN airlines ON flights.airline = airlines.id 
WHERE flights.ORIGIN_AIRPORT = :airport AND flights.DEPARTURE_DELAY >= 20
"""

QUERY_FLIGHTS_BY_DATE = """
SELECT flights.*, airlines.airline, flights.ID as FLIGHT_ID, flights.DEPARTURE_DELAY as DELAY 
FROM flights 
JOIN airlines ON flights.airline = airlines.id 
WHERE flights.YEAR = :year AND flights.MONTH = :month AND flights.DAY = :day
"""

QUERY_AVERAGE_DELAY_BY_AIRLINE = """
SELECT airlines.AIRLINE, avg(flights.DEPARTURE_DELAY) AS 'avg_delay'
FROM flights
JOIN airlines
ON flights.AIRLINE = airlines.ID
GROUP BY airlines.AIRLINE
ORDER BY avg(flights.DEPARTURE_DELAY) DESC;
"""



class FlightData:
    """
    The FlightData class is a Data Access Layer (DAL) object that provides an
    interface to the flight data in the SQLITE database. When the object is created,
    the class forms connection to the sqlite database file, which remains active
    until the object is destroyed.
    """
    def __init__(self, db_uri):
        """
        Initialize a new engine using the given database URI
        """
        self._engine = create_engine(db_uri)

    def __str__(self):
        return f"FlightData connected to {self.uri}"

    def __repr__(self):
        return f"FlightData(uri={self.uri})"


    def _execute_query(self, query, params):
        """
        Execute an SQL query with the params provided in a dictionary,
        and returns a list of records (dictionary-like objects).
        If an exception was raised, print the error, and return an empty list.
        """
        try:
            with self._engine.connect() as connection:
                results = connection.execute(text(query), params)
                rows = results.fetchall()
                return rows
        except Exception as e:
            return []


    def get_flight_by_id(self, flight_id):
        """
        Searches for flight details using flight ID.
        If the flight was found, returns a list with a single record.
        """
        params = {'id': flight_id}
        return self._execute_query(QUERY_FLIGHT_BY_ID, params)


    def get_delayed_flights_by_airline(self, airline):
        """
        Searches for delayed flights by airline name.
        """
        params = {'airline': airline}
        return self._execute_query(QUERY_DELAYED_FLIGHTS_BY_AIRLINE, params)


    def get_delayed_flights_by_airport(self, airport):
        """
        Searches for delayed flights by origin airport IATA code.
        """
        params = {'airport': airport}
        return self._execute_query(QUERY_DELAYED_FLIGHTS_BY_AIRPORT, params)


    def get_flights_by_date(self, day, month, year):
        """
        Searches for flights by date using separate day, month, and year columns.
        """
        params = {
            'year': year,
            'month': month,
            'day': day
        }

        return self._execute_query(QUERY_FLIGHTS_BY_DATE, params)


    def __del__(self):
        """
        Closes the connection to the database when the object is about to be destroyed
        """
        self._engine.dispose()
    