from sqlalchemy import create_engine, text

QUERY_FLIGHT_BY_ID = (
    "SELECT flights.*, airlines.airline, flights.ID as FLIGHT_ID,"
    + " flights.DEPARTURE_DELAY as DELAY FROM flights"
    + " JOIN airlines ON flights.airline = airlines.id WHERE flights.ID = :id;"
)
QUERY_FLIGHT_BY_DATE = (
        "SELECT FLIGHT_NUMBER AS ID,ORIGIN_AIRPORT,DESTINATION_AIRPORT,"
        + "airlines.AIRLINE, DEPARTURE_DELAY AS DELAY"
        + " FROM flights JOIN airlines ON flights.airline = airlines.id"
        + " WHERE DAY = :day AND MONTH = :month AND YEAR = :year;"
)
QUERY_FLIGHT_BY_AIRLINE = (
    "SELECT FLIGHT_NUMBER AS ID,ORIGIN_AIRPORT,DESTINATION_AIRPORT,"
    + "airlines.AIRLINE, DEPARTURE_DELAY AS DELAY"
    + " FROM flights JOIN airlines ON flights.AIRLINE = airlines.id"
    + " WHERE DELAY > 20 AND airlines.AIRLINE = :airline;"
)
QUERY_FLIGHT_BY_AIRPORT = (
    "SELECT FLIGHT_NUMBER AS ID,ORIGIN_AIRPORT,DESTINATION_AIRPORT,"
    + "airlines.AIRLINE, DEPARTURE_DELAY AS DELAY"
    + " FROM flights JOIN airlines ON flights.AIRLINE = airlines.id"
    + " JOIN airports ON flights.ORIGIN_AIRPORT = airports.IATA_CODE"
    + " WHERE DELAY > 20 AND airports.IATA_CODE = :airport;"
)
QUERY_DELAYED_FLIGHTS_BY_AIRLINES = (
    "SELECT air.AIRLINE AS airline,"
    + "(COUNT(CASE WHEN fly.DEPARTURE_DELAY > 20 THEN 1 END ) * 100.0 / COUNT(fly.FLIGHT_NUMBER))"
    + " AS delay_percentage"
    + " FROM airlines AS air"
    + " JOIN flights AS fly ON air.ID = fly.AIRLINE"
    + " GROUP BY air.AIRLINE;"
)
QUERY_DELAYED_FLIGHTS_BY_HOURS = (
    "SELECT CAST(SCHEDULED_DEPARTURE / 100 AS INTEGER) AS hour,"
    + " (COUNT(CASE WHEN DEPARTURE_DELAY > 20 THEN 1 END ) * 100.0 /"
    + " COUNT(*)) AS delay_percentage"
    + " FROM flights"
    + " GROUP BY hour"
    + " ORDER BY hour;"
)
QUERY_DELAYED_ROUTES = (
    "SELECT ORIGIN_AIRPORT AS origin, DESTINATION_AIRPORT as destination,"
    + " ORIGIN_AIRPORT || ' → ' || DESTINATION_AIRPORT AS flight_route,"
    + " (COUNT(CASE WHEN DEPARTURE_DELAY > 20 THEN 1 END) * 100.0 / COUNT(*)) AS delay_percentage"
    + " FROM flights"
    + " GROUP BY flight_route;"
)
QUERY_DELAYED_ROUTES_WITH_LON_LAT = (
    "SELECT o.LATITUDE AS origin_lat, o.LONGITUDE AS origin_lon,"
    + " d.LATITUDE AS destination_lat, d.LONGITUDE AS destination_lon,"
    + " ORIGIN_AIRPORT AS origin, DESTINATION_AIRPORT as destination,"
    + " ORIGIN_AIRPORT || ' → ' || DESTINATION_AIRPORT AS flight_route,"
    + " (COUNT(CASE WHEN DEPARTURE_DELAY > 20 THEN 1 END) * 100.0 / COUNT(*)) AS delay_percentage"
    + " FROM flights"
    + " JOIN airports AS o ON origin = o.IATA_CODE"
    + " JOIN airports AS d ON destination = d.IATA_CODE"
    + " GROUP BY flight_route;"
)


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


    def _execute_query(self, query, params):
        """
        Execute an SQL query with the params provided in a dictionary,
        and returns a list of records (dictionary-like objects).
        If an exception was raised, print the error, and return an empty list.
        """
        with self._engine.connect() as conn:
            return conn.execute(text(query), params).all()


    def get_flight_by_id(self, flight_id):
        """
        Searches for flight details using flight ID.
        If the flight was found, returns a list with a single record.
        """
        params = {'id': flight_id}
        return self._execute_query(QUERY_FLIGHT_BY_ID, params)


    def get_flights_by_date(self, day, month, year):
        """
        Searches for flights by date.
        If the flight was found, returns a list with a single record.
        """
        params = {'day': day, 'month': month, 'year': year}
        return self._execute_query(
            QUERY_FLIGHT_BY_DATE,
            params
        )


    def get_delayed_flights_by_airline(self, airline):
        """
        Searches for delayed flights by airline.
        If the flight was found, returns a list with a single record.
        """
        params = {'airline': airline}
        return self._execute_query(
            QUERY_FLIGHT_BY_AIRLINE,
            params
        )


    def get_delayed_flights_by_airport(self, airport):
        """
        Searches for delayed flights by airport.
        If the flight was found, returns a list with a single record.
        """
        params = {'airport': airport}
        return self._execute_query(
            QUERY_FLIGHT_BY_AIRPORT,
            params
        )


    def get_delayed_flights_by_airlines(self):
        """
        Searches for delayed flights by airline.
        Returns a list with all airlines and the percentage of delayed flights
        """
        with self._engine.connect() as conn:
            return conn.execute(text(QUERY_DELAYED_FLIGHTS_BY_AIRLINES)).all()


    def get_delayed_flights_by_hours(self):
        """
        Searches for delayed flights by hour.
        Returns a list with all hours and the percentage of delayed flights.
        """
        with self._engine.connect() as conn:
            return conn.execute(text(QUERY_DELAYED_FLIGHTS_BY_HOURS)).all()


    def get_delayed_routes(self):
        """
        Searches for delayed routes.
        returns a list with all flight routes and the percentage of delayed flights
        """
        with self._engine.connect() as conn:
            return conn.execute(text(QUERY_DELAYED_ROUTES)).all()


    def get_delayed_routes_with_lon_lat(self):
        """
        Searches for delayed routes.
        Returns a list with all flight routes and the percentage of delayed flights
        and the coordinates of the origin and destination airports
        """
        with self._engine.connect() as conn:
            return conn.execute(text(QUERY_DELAYED_ROUTES_WITH_LON_LAT)).all()

    def __del__(self):
        """
        Closes the connection to the databse when the object is about to be destroyed
        """
        self._engine.dispose()
