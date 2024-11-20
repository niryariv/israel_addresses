import pandas as pd
import pyproj
import sys

# Define the custom projection parameters for ITM (EPSG:2039) and WGS84 (EPSG:4326)
itm = pyproj.CRS(
    "+proj=tmerc +lat_0=31.7343936111111 +lon_0=35.2045169444444 +k=1.0000067 +x_0=219529.584 +y_0=626907.39 +ellps=GRS80 +towgs84=-24.0024,-17.1032,-17.8444,-0.33009,-1.85269,1.66969,5.4248 +units=m +no_defs"
)
wgs84 = pyproj.CRS("EPSG:4326")

# Transformer to convert from ITM to WGS84
transformer = pyproj.Transformer.from_crs(itm, wgs84, always_xy=True)

# Load the CSV file from command line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <input_file>")
    sys.exit(1)

input_file = sys.argv[1]
df = pd.read_csv(input_file)

# Ensure that the coordinates are treated as floats
df['X'] = pd.to_numeric(df['X'], errors='coerce')
df['Y'] = pd.to_numeric(df['Y'], errors='coerce')

# Drop rows with invalid (non-numeric) coordinates
df = df.dropna(subset=['X', 'Y'])

# Create new columns for latitude and longitude in WGS84
latitudes = []
longitudes = []

# Iterate through each row and convert the coordinates
for index, row in df.iterrows():
    x_itm, y_itm = row['X'], row['Y']
    lon, lat = transformer.transform(float(x_itm), float(y_itm))
    longitudes.append(lon)
    latitudes.append(lat)

# Add the new columns to the DataFrame
df['lon_WGS84'] = longitudes
df['lat_WGS84'] = latitudes

# Output the updated DataFrame to stdout
df.to_csv(sys.stdout, index=False)
