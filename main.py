import pandas as pd
import requests
import folium
import os


class Map:
    @staticmethod
    def DisplayMap():
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

        except Exception as e:
            print(f"Could not display map: {e}")


def FetchData():
    global results_df
    url = "https://data.cityofnewyork.us/resource/h9gi-nx95.json"

    try:
        n = int(input("How many records? "))
        if n <= 0:
            raise ValueError("Number of samples cannot be zero or negative.")
    except ValueError as ve:
        print(f"Input error: {ve}")
        return None

    params = {
        "$limit": 1000,
        "$offset": 0,
        "$order": "crash_date DESC"
    }

    total_records = 0
    results = []

    try:
        while total_records < n:
            current_limit = min(1000, n - total_records)
            params["$limit"] = current_limit
            params["$offset"] = total_records

            # Fetch data from API
            response = requests.get(url, params=params)

            # 🚨 DEBUGGING: Print HTTP status code 🚨
            print(f"API Response Code: {response.status_code}")

            if response.status_code != 200:
                print(f"Error: {response.status_code} - {response.text}")
                return None  # Stop function if API request fails

            # 🚨 DEBUGGING: Print raw API response 🚨
            try:
                batch = response.json()
                print("First 5 records:", batch[:5])  # Check structure
            except Exception as e:
                print(f"Failed to parse JSON: {e}")
                return None  # Stop function if JSON is invalid

            results.extend(batch)
            total_records += len(batch)

            if len(batch) < current_limit:
                break

        print(f"Fetched {len(results)} records.")

        # ✅ Ensure DataFrame is created outside of exception block
        if results:
            results_df = pd.DataFrame(results)
            print(f"✅ DataFrame Shape: {results_df.shape}")  # Should show (n, columns)

            # Define output directory and file
            output_dir = r"C:\Users\user\Documents\My stuff\Hobbies\Programming\NYC Traffic project\Data"
            os.makedirs(output_dir, exist_ok=True)  # Ensure directory exists
            output_file = os.path.join(output_dir, "output.csv")

            # Save DataFrame to CSV
            results_df.to_csv(output_file, index=False)
            print(f"✅ Data successfully saved to {output_file}")

    except requests.exceptions.RequestException as re:
        print(f"API error: {re}")
    except Exception as e:
        print(f"Unexpected error: {e}")


Map.DisplayMap()
FetchData()

# ------------------DATA PREPARATION IN PANDAS------------------------
output_dir = r"C:\Users\user\Documents\My stuff\Hobbies\Programming\Projects\NYC Traffic project\Data"
file = os.path.join(output_dir, "output.csv")

try:
    df = pd.read_csv(file, delimiter=',', header=0, encoding='utf-8')
    print("Original DataFrame loaded successfully.")

    if 'location' in df.columns:
        df.drop(columns='location', inplace=True)
        print("Dropped 'location' column.")

    output_file = os.path.join(output_dir, 'output_clean.csv')
    df.to_csv(output_file, index=False)
    print(f"Modified DataFrame saved to {output_file}")

except FileNotFoundError:
    print(f"Error: {file} not found. Make sure FetchData() ran successfully.")
except Exception as e:
    print(f"Error processing data: {e}")

r"""
# Permissions Test:
test_path = r"C:\Users\user\Documents\My stuff\Hobbies\Programming\Projects\NYC Traffic project\Data"
try:
    with open(test_path, "w") as f:
        f.write("Test file created successfully!")
    print(f"Test file created at {test_path}")
except Exception as e:
    print(f"Failed to write test file: {e}")
"""

print(results_df)
