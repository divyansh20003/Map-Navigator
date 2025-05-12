import gradio as gr
from map_generator import MapGenerator
from route_calculator import RouteCalculator

# Enter your OpenRouteService API key here
ORS_API_KEY = '5b3ce3597851110001cf6248433a79debdc24d60a3f04060020f32b4'

# Create an instance of RouteCalculator
route_calculator = RouteCalculator(api_key=ORS_API_KEY)


# Gradio function that calculates and displays the interactive map and routes
def calculate_route(start_address, end_address, intermediate_addresses, mode, selected_indices):
    try:
        # Geocode the start, intermediate, and end addresses
        start_coords = route_calculator.geocode_address(start_address)
        end_coords = route_calculator.geocode_address(end_address)

        intermediate_coords = []

        # Check if intermediate addresses are provided
        if intermediate_addresses:
            for address in intermediate_addresses.split(','):
                coords = route_calculator.geocode_address(address.strip())
                if coords:
                    intermediate_coords.append(coords)

        if not start_coords:
            return f"Could not find location for: {start_address}"
        if not end_coords:
            return f"Could not find location for: {end_address}"

        # Combine all coordinates: start, intermediates (if any), and end
        coords_list = [start_coords] + intermediate_coords + [end_coords]

        # Convert selected_indices string to list of integers
        try:
            selected_indices = [int(i.strip()) for i in selected_indices.split(',') if i.strip()]
        except ValueError:
            return "Error: Please enter valid indices (comma-separated)."

        # Check if the user has selected specific locations, otherwise display interactive map
        if not selected_indices:
            return MapGenerator.create_interactive_map(coords_list)

        # Map the selected mode to OpenRouteService profile
        mode_map = {
            "Driving": "driving-car",
            "Walking": "foot-walking",
            "Cycling": "cycling-regular"
        }
        mode = mode_map.get(mode, "driving-car")

        # Calculate the route
        route_coords, distance, duration_time = route_calculator.calculate_route(
            [coords_list[i] for i in selected_indices], mode)

        if route_coords is None:
            return distance  # Return the error message if route calculation failed

        # Display the route map
        return MapGenerator.display_route_map(
            [coords_list[i] for i in selected_indices], route_coords, distance, duration_time)

    except Exception as e:
        return f"An unexpected error occurred while calculating the route: {e}"


# Gradio interface for input and display
def interactive_map_ui():
    iface = gr.Interface(
        fn=calculate_route,
        inputs=[
            gr.Textbox(label="Start Address", placeholder="Enter start address here"),
            gr.Textbox(label="End Address", placeholder="Enter end address here"),
            gr.Textbox(label="Intermediate Addresses (comma-separated)",
                       placeholder="Optional: Enter intermediate addresses here, separated by commas"),
            gr.Dropdown(["Driving", "Walking", "Cycling"], label="Mode of Travel", value="Driving"),
            gr.Textbox(label="Selected Indices (comma-separated)",
                       placeholder="Enter the indices of the locations you want to connect, e.g., '0,1,3'")
        ],
        outputs=gr.Markdown(),
        title="Multi-Stop Interactive Route Finder",
        description="Enter your start, intermediate (optional), and end addresses. "
                    "Select locations from the map to calculate the route between them."
    )

    # Launch Gradio UI
    iface.launch(share=True)


# Run the Gradio UI
interactive_map_ui()
