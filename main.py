import pandas as pd
import requests
import NYC_Map
import os
from concurrent.futures import ThreadPoolExecutor, as_completed


def fetch_batch(url, limit, offset):
    '''' Fetch a single batch of data from the API'''
    params = {
        "$limit": limit,
        "$offset": offset,
        "$order": "crash_date DESC"
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text} ")
        return []


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

    total_records = 0
    results = []
    batch_size = 1000 # Maximum limit per request

    # Determine number of batches

    num_batches = (n // batch_size) + (1 if n % batch_size !=0 else 0)
    offsets = [i*batch_size for i in range(num_batches)]

    print(f"Fetching {n} records in {num_batches} parallel requests...")

    # Use ThreadPoolExecutor fof parallel API requests
    with ThreadPoolExecutor(max_workers=5) as executor: # Adjust workers if needed
        future_to_offset = {executor.submit(fetch_batch, url, batch_size, offset):
                            offset for offset in offsets}

        for future in as_completed(future_to_offset):
            batch = future.result()
            results.extend(batch)
            total_records += len(batch)

            # ✅ Fix: Stop only if we have at least `n` records
            if total_records >= n:
                results = results[:n]  # Ensure we don't exceed `n`
                break

    print(f" Fetched {len(results)} records.")

    if results:
            results_df = pd.DataFrame(results)
            print(f" DataFrame Shape: {results_df.shape}")  # Should show (n, columns)

            # Define output directory and file
            output_dir = r"C:\Users\user\Documents\My stuff\Hobbies\Programming\Projects\NYC Traffic project\Data"
            os.makedirs(output_dir, exist_ok=True)  # Ensure directory exists
            output_file = os.path.join(output_dir, "output.csv")

            # Save DataFrame to CSV
            results_df.to_csv(output_file, index=False)
            print(f"✅ Data successfully saved to {output_file}")

    return results_df


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


print(results_df)


