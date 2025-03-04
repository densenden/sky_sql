# visualization.py
import matplotlib.pyplot as plt

def plot_delayed_flights_percentage(data_manager):
    """
    Plots the percentage of delayed flights per airline.
    """
    # Query to get the total number of flights per airline
    total_flights_query = """
    SELECT airlines.airline, COUNT(flights.ID) as total_flights
    FROM flights
    JOIN airlines ON flights.airline = airlines.id
    GROUP BY airlines.airline
    """

    # Query to get the number of delayed flights per airline
    delayed_flights_query = """
    SELECT airlines.airline, COUNT(flights.ID) as delayed_flights
    FROM flights
    JOIN airlines ON flights.airline = airlines.id
    WHERE flights.DEPARTURE_DELAY > 0
    GROUP BY airlines.airline
    """

    total_flights = data_manager._execute_query(total_flights_query, {})
    delayed_flights = data_manager._execute_query(delayed_flights_query, {})

    # Convert results to dictionaries for easier access
    total_flights_dict = {row[0]: row[1] for row in total_flights}
    delayed_flights_dict = {row[0]: row[1] for row in delayed_flights}

    airlines = list(total_flights_dict.keys())
    percentages = [(delayed_flights_dict.get(airline, 0) / total_flights_dict[airline]) * 100 for airline in airlines]

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.bar(airlines, percentages, color='skyblue')
    plt.xlabel('Airline')
    plt.ylabel('Percentage of Delayed Flights')
    plt.title('Percentage of Delayed Flights per Airline')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()