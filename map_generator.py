import folium
import webbrowser
import os
from folium.plugins import MarkerCluster


class MapGenerator:
    def __init__(self):
        pass

    @staticmethod
    def create_interactive_map(coords_list):
        try:
            # Create a folium map centered on the first coordinates
            m = folium.Map(location=coords_list[0], zoom_start=12)

            # Add markers to the map using a MarkerCluster for easy selection
            marker_cluster = MarkerCluster().add_to(m)
            for i, coords in enumerate(coords_list):
                folium.Marker(location=coords, popup=f"Location {i + 1}",
                              icon=folium.Icon(color="blue")).add_to(marker_cluster)

            # Save the map as an HTML file
            map_file = 'interactive_map.html'
            m.save(map_file)

            if os.path.exists(map_file):
                # Open the map in the default web browser
                webbrowser.open(f"file://{os.path.abspath(map_file)}", new=2)
                return "Interactive map opened in the browser. Select the points and re-run the process."
            else:
                return "Error: Failed to generate the map."
        except Exception as e:
            return f"Error while creating the map: {e}"

    @staticmethod
    def display_route_map(selected_coords, route_coords, distance, duration_time):
        try:
            # Create a folium map centered on the first selected coordinates
            m = folium.Map(location=selected_coords[0], zoom_start=12)

            # Add markers for the selected locations
            for i, coords in enumerate(selected_coords):
                folium.Marker(location=coords, popup=f"Selected Location {i + 1}",
                              icon=folium.Icon(color="green")).add_to(m)

            # Draw the route on the map
            folium.PolyLine(locations=[(lat, lon) for lon, lat in route_coords],
                            color="blue", weight=2.5, opacity=1).add_to(m)

            # Save the map as an HTML file
            map_file = 'selected_route_map.html'
            m.save(map_file)

            if os.path.exists(map_file):
                # Open the map directly in the default web browser
                webbrowser.open(f"file://{os.path.abspath(map_file)}", new=2)
                return (f"Total Distance: {distance:.2f} km\n Total Duration:{duration_time}\n "
                        f"The map has been opened in the browser.")
            else:
                return "Error: Failed to generate the map."
        except Exception as e:
            return f"Error while displaying the route map: {e}"
