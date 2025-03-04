import matplotlib.pyplot as plt
import plotly.graph_objects as go


class FlightDataVisualizer:
    def __init__(self, data_manager):
        self.data_manager = data_manager

    def plot_delayed_flights_percentage(self):
        """
        Plots the percentage of delayed flights per airline.
        """
        total_flights_query = """
        SELECT airlines.airline, COUNT(flights.ID) as total_flights
        FROM flights
        JOIN airlines ON flights.airline = airlines.id
        GROUP BY airlines.airline
        """

        delayed_flights_query = """
        SELECT airlines.airline, COUNT(flights.ID) as delayed_flights
        FROM flights
        JOIN airlines ON flights.airline = airlines.id
        WHERE flights.DEPARTURE_DELAY > 0
        GROUP BY airlines.airline
        """

        total_flights = self.data_manager._execute_query(total_flights_query, {})
        delayed_flights = self.data_manager._execute_query(delayed_flights_query, {})

        total_flights_dict = {row[0]: row[1] for row in total_flights}
        delayed_flights_dict = {row[0]: row[1] for row in delayed_flights}

        airlines = list(total_flights_dict.keys())
        percentages = [(delayed_flights_dict.get(airline, 0) / total_flights_dict[airline]) * 100 for airline in airlines]

        plt.figure(figsize=(10, 6))
        plt.bar(airlines, percentages, color='skyblue')
        plt.xlabel('Airline')
        plt.ylabel('Percentage of Delayed Flights')
        plt.title('Percentage of Delayed Flights per Airline')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()

    def plot_delayed_flights_by_hour(self):
        """
        Plots the percentage of delayed flights per hour of the day using Plotly.
        """
        total_flights_query = """
        SELECT strftime('%H', flights.DEPARTURE_TIME) as hour, COUNT(flights.ID) as total_flights
        FROM flights
        GROUP BY hour
        """

        delayed_flights_query = """
        SELECT strftime('%H', flights.DEPARTURE_TIME) as hour, COUNT(flights.ID) as delayed_flights
        FROM flights
        WHERE flights.DEPARTURE_DELAY > 0
        GROUP BY hour
        """

        total_flights = self.data_manager._execute_query(total_flights_query, {})
        delayed_flights = self.data_manager._execute_query(delayed_flights_query, {})

        total_flights_dict = {row[0]: row[1] for row in total_flights if row[0] is not None}
        delayed_flights_dict = {row[0]: row[1] for row in delayed_flights if row[0] is not None}

        hours = list(total_flights_dict.keys())
        percentages = [(delayed_flights_dict.get(hour, 0) / total_flights_dict[hour]) * 100 for hour in hours]

        colors = ['rgba(0, 0, 255, {:.2f})'.format(percentage / 100) for percentage in percentages]

        fig = go.Figure(data=[go.Bar(x=hours, y=percentages, marker_color=colors)])
        fig.update_layout(
            title='Percentage of Delayed Flights per Hour of the Day',
            xaxis_title='Hour of the Day',
            yaxis_title='Percentage of Delayed Flights',
            template='plotly_white'
        )
        fig.show()