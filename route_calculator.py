import openrouteservice


class RouteCalculator:
    def __init__(self, api_key):
        self.client = openrouteservice.Client(key=api_key)

    def geocode_address(self, address):
        try:
            geocode_result = self.client.pelias_search(text=address)
            if geocode_result and 'features' in geocode_result and geocode_result['features']:
                coords = geocode_result['features'][0]['geometry']['coordinates']
                return coords[1], coords[0]  # Return (latitude, longitude)
            else:
                return None
        except Exception as e:
            print(f"Geocoding error for {address}: {e}")
            return None

    def calculate_route(self, selected_coords, mode):
        try:
            # Request the route between the selected points with the selected travel mode
            routes = self.client.directions(
                coordinates=[(lon, lat) for lat, lon in selected_coords],
                profile=mode,
                format='geojson'
            )

            if 'features' not in routes or not routes['features']:
                return None, None, "Error: No routes found."

            geometry = routes['features'][0]['geometry']
            route_coords = geometry['coordinates']

            distance = routes['features'][0]['properties']['segments'][0]['distance'] / 1000  # in kilometers
            duration_sec = routes['features'][0]['properties']['segments'][0]['duration']  # in seconds
            # Calculate duration in hours and minutes
            hours, remainder = divmod(duration_sec, 3600)
            minutes, _ = divmod(remainder, 60)
            duration_time = f"{int(hours)}h {int(minutes)}m"  # Format as 'Xh Ym'

            return route_coords, distance, duration_time
        except openrouteservice.exceptions.ApiError as api_error:
            return None, None, f"API Error: {api_error}"
        except openrouteservice.exceptions.HTTPError as http_error:
            return None, None, f"HTTP Error: {http_error}"
        except Exception as e:
            return None, None, f"An unexpected error occurred: {e}"
