import matplotlib.pyplot as plt
from matplotlib import colors
import matplotlib.cm as cm
import pandas as pd
import seaborn as sns
import geopandas as gpd
from shapely.geometry import Point, LineString
from matplotlib.colors import Normalize



def plot_delayed_flights_by_airlines(dataset):
    """
    Plots a histogram of the percentage of delayed flights by airline
    """
    # data for the histogram
    names = [dat['airline'] for dat in dataset]
    values = [dat['delay_percentage'] for dat in dataset]

    # Plotting a basic histogram
    plt.figure(figsize=(8, 4))  # Adjust figure size for readability
    plt.bar(names, values, color='skyblue', edgecolor='black')

    # Rotate x-axis labels
    plt.xticks(rotation=45, ha="right")
    # Adding labels and title
    plt.xlabel('Airlines')
    plt.ylabel('Percentage of delayed flights')
    plt.title('Delay by airlines Histogram')

    # Display the plot
    plt.show()


def plot_delayed_flights_by_hours(dataset):
    """
    Plots a bar chart of the percentage of delayed flights by hour with a colorbar.
    """
    # Extract data
    names = [dat['hour'] for dat in dataset]
    values = [dat['delay_percentage'] for dat in dataset]

    # Normalize values for color mapping
    norm = colors.Normalize(vmin=min(values), vmax=max(values))
    cmap = cm.viridis  # Using Viridis colormap

    # Create figure
    fig, ax = plt.subplots(figsize=(10, 7), tight_layout=True)

    # Create bars with colors based on delay percentage
    bars = ax.bar(names, values, color=cmap(norm(values)))

    # Add colorbar
    sm = cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])  # Dummy array for colorbar
    cbar = plt.colorbar(sm, ax=ax)
    cbar.set_label("Delay Percentage (%)")

    # Styling
    ax.set_xlabel("Hours")
    ax.set_ylabel("Delay Percentage")
    ax.set_title("Delay by Hours")

    # Show plot
    plt.show()


def plot_delayed_routes_as_heatmap(dataset):
    """
    Plots Hexbin plot of the percentage of delayed flights by route
    """
    # Convert dataset to DataFrame
    # Convert dataset to DataFrame
    df = pd.DataFrame(dataset)

    # Create a pivot table with origins as columns, destinations as rows
    pivot_table = df.pivot(index="destination", columns="origin", values="delay_percentage")

    # Set up the figure
    plt.figure(figsize=(6, 6))

    # Create the heatmap
    sns.heatmap(
        pivot_table,
        cmap="Blues",  # Color intensity for delays
        annot=False,  # Show delay percentages inside cells
        fmt=".1f",  # Format to 1 decimal place
        linewidths=0.5,  # Add lines between cells for clarity
        cbar=True  # Show colorbar
    )

    # Labels and title
    plt.xlabel("Origin Airport")
    plt.ylabel("Destination Airport")
    plt.title("Flight Route Delay Percentage Heatmap")

    # Rotate x-axis labels for readability
    plt.xticks(rotation=45, ha="right")

    # Show plot
    plt.show()


def plot_route_delays_usa_map(dataset):
    """
    Plots flight routes on a USA map based on provided coordinates (lat, lon) for origin and destination airports.
    """
    # Load the world shapefile
    shapefile_path = "data/ne_110m_admin_0_countries.shp"  # Replace with your actual shapefile path
    world = gpd.read_file(shapefile_path)
    # Select only the USA (note the corrected value for "SOVEREIGNT")
    usa = world[world["SOVEREIGNT"] == "United States of America"]

    # Create a GeoDataFrame for flight routes
    flight_lines = []  # Use a list to collect flight route data efficiently
    for flight in dataset:
        # Create LineStrings for each flight route
        origin = Point(flight["origin_lon"], flight["origin_lat"])
        destination = Point(flight["destination_lon"], flight["destination_lat"])
        flight_line = LineString([origin, destination])
        flight_lines.append({"geometry": flight_line, "delay_percentage": flight['delay_percentage']})

    # Combine all collected flight lines into a single GeoDataFrame
    gdf = gpd.GeoDataFrame(flight_lines, crs="EPSG:4326")

    # Plot the USA map without Alaska
    fig, ax = plt.subplots(figsize=(9, 6))

    # Plot the USA layer
    usa.plot(ax=ax, color="lightgrey", edgecolor="black")

    # Normalize delay_percentage for the colormap (values between 0 and 100)
    norm = colors.Normalize(vmin=0, vmax=100)
    colormap = plt.cm.Blues  # Use the Blues colormap

    # Plot flight routes with a color scale
    gdf.plot(ax=ax, linewidth=2, color=gdf['delay_percentage'].apply(lambda x: colormap(norm(x))))

    # Add labels for airports
    for flight in dataset:
        ax.text(flight["origin_lon"], flight["origin_lat"], flight["origin"], fontsize=9, ha='center', color='black')
        ax.text(flight["destination_lon"], flight["destination_lat"], flight["destination"], fontsize=9, ha='center',
                color='black')

    # Add colorbar
    sm = plt.cm.ScalarMappable(cmap='Blues', norm=norm)
    cbar = fig.colorbar(sm, ax=ax, orientation="vertical", fraction=0.02, pad=0.04)
    cbar.set_label('Delay Percentage')

    # Title and labels
    ax.set_title("Flight Routes with Delay Percentages", fontsize=16)
    plt.show()
