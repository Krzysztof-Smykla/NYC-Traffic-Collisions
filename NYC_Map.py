import folium
import os
import webbrowser


class Map:
    @staticmethod
    def GenerateMap():
        try:
            # Define map center coordinates for NYC
            nyc_coordinates = (40.7128, -74.0060)

            # Create a folium map centered on NYC
            m = folium.Map(location=nyc_coordinates, zoom_start=12)

            # Define the directory and file name
            directory = r"C:\Users\user\Documents\My stuff\Hobbies\Programming\NYC Traffic project\Data"
            file_name = "nyc_map.html"

            # Ensure the directory exists
            os.makedirs(directory, exist_ok=True)

            # Create the full file path
            path = os.path.join(directory, file_name)

            # Save the map correctly
            m.save(path)

            # Check if the file was successfully created
            if os.path.exists(path):
                print(f"Map saved successfully at: {path}")
            else:
                print("Error: Map file not found. Please check the file path.")

            return path
        except Exception as e:
            print(f"Could not display map: {e}")

            return None

    @classmethod
    def DisplayMap(cls, map_path):
        if map_path and os.path.exists(map_path):
            webbrowser.open(map_path)
        else:
            print("Error: Map file not found or path is invalid.")

map_file = Map.GenerateMap()
Map.DisplayMap(map_file)