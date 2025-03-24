from sqlalchemy import create_engine, text

QUERY_FLIGHT_BY_ID = (
    "SELECT flights.*, airlines.airline, flights.ID as FLIGHT_ID,"
    + " flights.DEPARTURE_DELAY as DELAY FROM flights"
    + " JOIN airlines ON flights.airline = airlines.id WHERE flights.ID = :id"
)
QUERY_FLIGHT_BY_DATE = (
        "SELECT FLIGHT_NUMBER AS ID,ORIGIN_AIRPORT,DESTINATION_AIRPORT,airlines.AIRLINE, DEPARTURE_DELAY AS DELAY"
        + " FROM flights JOIN airlines ON flights.airline = airlines.id"
        + " WHERE DAY = :day AND MONTH = :month AND YEAR = :year"
)
QUERY_FLIGHT_BY_AIRLINE = (
    "SELECT FLIGHT_NUMBER AS ID,ORIGIN_AIRPORT,DESTINATION_AIRPORT,airlines.AIRLINE, DEPARTURE_DELAY AS DELAY"
    + " FROM flights JOIN airlines ON flights.AIRLINE = airlines.id"
    + " WHERE DELAY > 20 AND airlines.AIRLINE = :airline"
)
QUERY_FLIGHT_BY_AIRPORT = (
    "SELECT FLIGHT_NUMBER AS ID,ORIGIN_AIRPORT,DESTINATION_AIRPORT,airlines.AIRLINE, DEPARTURE_DELAY AS DELAY"
    + " FROM flights JOIN airlines ON flights.AIRLINE = airlines.id"
    + " WHERE DELAY > 20 AND ORIGIN_AIRPORT = :airport"
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


    def __del__(self):
        """
        Closes the connection to the databse when the object is about to be destroyed
        """
        self._engine.dispose()
    