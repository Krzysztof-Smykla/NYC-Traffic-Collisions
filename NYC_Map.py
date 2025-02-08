import tempfile

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

            # Debugging: Check if 'm' is a valid Folium map
            if isinstance(m, folium.Map):
                print("✅ Folium map generated successfully.")
            else:
                print("❌ 'm' is not a valid Folium map object.")
                return None

            # Define the directory and file name
            directory = r"C:\Users\user\Documents\My stuff\Hobbies\Programming\Projects\NYC Traffic project\Data"
            file_name = "nyc_map.html"

            # Ensure the directory exists
            os.makedirs(directory, exist_ok=True)

            # Create the full file path
            path = os.path.join(directory, file_name)

            # Save the map correctly
            m.save(path)

            # Check if the file was successfully created
            if os.path.exists(path):
                print(f"✅ Map saved successfully at: {path}")
            else:
                print("❌ Error: Map file not found. Please check the file path.")

            return m
        except Exception as e:
            print(f"❌ Could not display map: {e}")
            return None


    @classmethod
    def DisplayMap(cls, m):
        """ Opens the folium map `m` directly in the browser """
        if isinstance(m, folium.Map):
            # Create a temporary file to store the map's HTML
            with tempfile.NamedTemporaryFile(delete=False, suffix='.html') as tmp_file:
                tmp_file_path = tmp_file.name
                m.save(tmp_file_path)  # Save the map HTML to the temporary file

            # Open the temporary map file in the default browser
            webbrowser.open(f'file:///{tmp_file_path}')
            print(f"✅ Opening map from generated object: {tmp_file_path}")
        else:
            print("❌ Error: The provided object is not a valid Folium map.")

