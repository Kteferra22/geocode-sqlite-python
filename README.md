🌍 Geolocation Mapping with Python and SQLite
This project retrieves geographic coordinates from an API based on a list of addresses, stores the data in an SQLite database, and creates a JavaScript file to visualize those locations on a map.

✅ Prerequisites

Python 3 installed

Internet connection

A file named where.data with a list of locations (one per line)

📘 Steps to Use the Project

🔹 STEP 1: Import required modules

The script imports Python modules like urllib, sqlite3, json, and ssl to handle web access, database storage, and secure connections.

🔹 STEP 2: Set up the API endpoint

The base URL is defined:

serviceurl = 'https://py4e-data.dr-chuck.net/opengeo?'

This API will be used to retrieve geolocation data.

🔹 STEP 3: Create/open the SQLite database

A database opengeo.sqlite is created with a table Locations containing two fields:

address: the place name

geodata: the full JSON response from the API

🔹 STEP 4: Configure SSL context

SSL settings are adjusted to ignore certificate validation errors, which ensures web requests won’t crash due to unverified HTTPS connections.

🔹 STEP 5: Read input file

The script reads a file named where.data that lists addresses to be geocoded.

🔹 STEP 6: Check cache to avoid redundant API calls

Before making an API request, the script checks if the location is already stored in the database.

🔹 STEP 7: Retrieve geolocation data from the API

If not in the cache, the script calls the API, retrieves the geodata, and stores it in the database.

🔹 STEP 8: Limit API calls and handle errors

Maximum 100 addresses processed per run

API call errors and empty results are handled gracefully

Script pauses after every 10 requests to avoid overloading the server

🔹 STEP 9: Convert saved data into a JavaScript array

A second script (geodump.py) reads the stored data, parses the JSON, and extracts:

latitude

longitude

place name

This info is saved into where.js in the format needed for mapping.

🔹 STEP 10: View your data on a map

After generating where.js, open where.html in a browser to see your mapped locations!

📂 Output Files

opengeo.sqlite – Local database storing geolocation info

where.js – JavaScript array of coordinates for mapping

where.html – (Provided in course repo) to visualize the results on a map
