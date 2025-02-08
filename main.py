import pandas as pd
import requests
import NYC_Map
import folium
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

# 🔹 Define Global Directory for Reusability
BASE_DIR = r"C:\Users\user\Documents\My stuff\Hobbies\Programming\Projects\NYC Traffic project\Data"


def fetch_batch(url, limit, offset):
    ''' Fetch a single batch of data from the API '''
    params = {
        "$limit": limit,
        "$offset": offset,
        "$order": "crash_date DESC"
    }
    response = requests.get(url, params=params)
    return response.json() if response.status_code == 200 else []


def FetchData():
    global results_df
    url = "https://data.cityofnewyork.us/resource/h9gi-nx95.json"

    try:
        n = int(input("How many records? "))
        if n <= 0:
            raise ValueError("Number of samples cannot be zero or negative.")
    except ValueError as ve:
        print(f"❌ Input error: {ve}")
        return None

    total_records, results = 0, []
    batch_size = 1000
    offsets = [i * batch_size for i in range((n // batch_size) + (1 if n % batch_size != 0 else 0))]

    print(f"Fetching {n} records...")

    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_offset = {executor.submit(fetch_batch, url, batch_size, offset): offset for offset in offsets}

        for future in as_completed(future_to_offset):
            batch = future.result()
            results.extend(batch)
            total_records += len(batch)
            if total_records >= n:
                results = results[:n]
                break

    print(f"✅ Fetched {len(results)} records.")

    if results:
        results_df = pd.DataFrame(results)
        output_file = os.path.join(BASE_DIR, "output.csv")
        results_df.to_csv(output_file, index=False)
        print(f"✅ Data successfully saved to {output_file}")

    return results_df


def PopulateMap(clean):
    if os.path.splitext(clean)[1].lower() != ".csv":
        print("❌ This is NOT a CSV file.")
        return 0

    df = pd.read_csv(clean)

    # ✅ Handle missing latitude/longitude
    if "latitude" in df.columns and "longitude" in df.columns:
        df = df.dropna(subset=["latitude", "longitude"])
        df["latitude"] = df["latitude"].astype(float)
        df["longitude"] = df["longitude"].astype(float)
    elif "location" in df.columns:
        df[["latitude", "longitude"]] = df["location"].str.strip("()").str.split(",", expand=True).astype(float)
        df.drop(columns=["location"], inplace=True)
    else:
        raise ValueError("❌ CSV must contain 'latitude' and 'longitude'.")

    # ✅ Generate the map
    m = NYC_Map.Map.GenerateMap()
    if not isinstance(m, folium.Map):
        raise TypeError("❌ 'm' is not a valid Folium map object.")

    # ✅ Add Markers
    for _, row in df.iterrows():
        popup_text = row["name"] if "name" in df.columns else "Unknown Location"
        tooltip_text = row["name"] if "name" in df.columns else "Unknown Location"

        folium.Marker(
            location=[row["latitude"], row["longitude"]],
            popup=popup_text,
            tooltip=tooltip_text,
            icon=folium.Icon(color="blue", icon="info-sign")
        ).add_to(m)

    map_file = os.path.join(BASE_DIR, "nyc_map.html")
    m.save(map_file)
    print(f"✅ Map updated and saved to {map_file}")

    return m  # Return the map object instead of the file path


# 🔹 Fetch Data and Clean It
FetchData()
output_csv = os.path.join(BASE_DIR, "output.csv")

try:
    df = pd.read_csv(output_csv, encoding='utf-8')
    print("✅ Original DataFrame loaded successfully.")

    if 'location' in df.columns:
        df.drop(columns='location', inplace=True)
        print("✅ Dropped 'location' column.")

    output_clean = os.path.join(BASE_DIR, 'output_clean.csv')
    if not os.path.exists(output_clean):
        df.to_csv(output_clean, index=False)
        print(f"✅ Cleaned DataFrame saved to {output_clean}")

except FileNotFoundError:
    print(f"❌ Error: {output_csv} not found. Make sure FetchData() ran successfully.")
except Exception as e:
    print(f"❌ Error processing data: {e}")

# 🔹 Generate and Display map
m = PopulateMap(output_clean)  # Now we get the map object directly from PopulateMap
if m:
    NYC_Map.Map.DisplayMap(m)  # Use the map object `m` for display
