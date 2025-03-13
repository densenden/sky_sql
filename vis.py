# vis.py
import plotly.graph_objects as go
import matplotlib.pyplot as plt


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
        percentages = [(delayed_flights_dict.get(airline, 0) / total_flights_dict[airline]) * 100 for airline in
                       airlines]

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
        SELECT CAST(substr(flights.DEPARTURE_TIME, 1, 2) AS INTEGER) as hour,
               COUNT(flights.ID) as total_flights
        FROM flights
        GROUP BY hour
        ORDER BY hour
        """

        delayed_flights_query = """
        SELECT CAST(substr(flights.DEPARTURE_TIME, 1, 2) AS INTEGER) as hour,
               COUNT(flights.ID) as delayed_flights
        FROM flights
        WHERE flights.DEPARTURE_DELAY > 0
        GROUP BY hour
        ORDER BY hour
        """

        total_flights = self.data_manager._execute_query(total_flights_query, {})
        delayed_flights = self.data_manager._execute_query(delayed_flights_query, {})

        total_flights_dict = {str(hour).zfill(2): 0 for hour in range(24)}
        delayed_flights_dict = {str(hour).zfill(2): 0 for hour in range(24)}

        for row in total_flights:
            if row[0] is not None:
                hour = str(row[0]).zfill(2)
                total_flights_dict[hour] = row[1]

        for row in delayed_flights:
            if row[0] is not None:
                hour = str(row[0]).zfill(2)
                delayed_flights_dict[hour] = row[1]

        hours = list(total_flights_dict.keys())
        percentages = [
            (delayed_flights_dict[hour] / total_flights_dict[hour]) * 100
            if total_flights_dict[hour] > 0 else 0
            for hour in hours
        ]

        fig = go.Figure(data=[go.Bar(x=hours, y=percentages)])
        fig.update_layout(
            title='Percentage of Delayed Flights per Hour of the Day',
            xaxis_title='Hour of the Day',
            yaxis_title='Percentage of Delayed Flights',
            template='plotly_white'
        )
        fig.show()

    def plot_delayed_flights_by_route(self):
        """
        Plots flight routes on a map with delay percentages.
        """
        token = "pk.eyJ1IjoicGxvdGx5bWFwYm94IiwiYSI6ImNrOWJqb2F4djBnMjEzbG50amg0dnJieG4ifQ.Zme1-Uzoi75IaFbieBDl3A"

        route_query = """
        SELECT
            o.LATITUDE as origin_lat,
            o.LONGITUDE as origin_lon,
            d.LATITUDE as dest_lat,
            d.LONGITUDE as dest_lon,
            o.IATA as origin_iata,
            d.IATA as dest_iata,
            COUNT(*) as total_flights,
            ROUND(AVG(CASE WHEN f.DEPARTURE_DELAY > 0 THEN 1 ELSE 0 END) * 100, 1) as delay_percentage
        FROM flights f
        JOIN airports o ON f.ORIGIN_AIRPORT = o.IATA
        JOIN airports d ON f.DESTINATION_AIRPORT = d.IATA
        GROUP BY o.IATA, d.IATA, o.LATITUDE, o.LONGITUDE, d.LATITUDE, d.LONGITUDE
        HAVING total_flights > 10
        """

        routes = self.data_manager._execute_query(route_query, {})

        if not routes:
            print("No data retrieved from the query.")
            return

        fig = go.Figure()

        for route in routes:
            origin_lat, origin_lon, dest_lat, dest_lon, origin_iata, dest_iata, flights, delay_pct = route

            if None in (origin_lat, origin_lon, dest_lat, dest_lon):
                continue

            color = f'rgb(255, {max(0, int(255 * (1 - delay_pct / 100)))}, 0)'

            fig.add_trace(
                go.Scattermapbox(
                    lon=[origin_lon, dest_lon],
                    lat=[origin_lat, dest_lat],
                    mode='lines+markers',
                    line=dict(width=1, color=color),
                    marker=dict(size=4),
                    name=f"{origin_iata}-{dest_iata}",
                    hovertemplate=f"Route: {origin_iata} → {dest_iata}<br>Delays: {delay_pct}%<extra></extra>"
                )
            )

        fig.update_layout(
            mapbox=dict(
                accesstoken=token,
                style="open-street-map",
                zoom=3,
                center=dict(lat=39.8, lon=-98.5)
            ),
            showlegend=False,
            margin=dict(r=0, t=30, l=0, b=0),
            title="Flight Routes Delay Percentages"
        )

        fig.show()
