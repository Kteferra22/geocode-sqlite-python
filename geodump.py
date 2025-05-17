## Step 1: Import required modules
import sqlite3    # for interacting with SQLite databases
import json       # for parsing JSON data
import codecs     # for writing UTF-8 encoded text files

## Step 2: Connect to the SQLite database
database_connection = sqlite3.connect('opengeo.sqlite')  # connect to the existing database
db_cursor = database_connection.cursor()  # create a cursor to execute SQL queries

## Step 3: Prepare to write the JavaScript output
db_cursor.execute('SELECT * FROM Locations')  # retrieve all records from the Locations table
output_file = codecs.open('where.js', 'w', "utf-8")  # open output JS file with UTF-8 encoding
output_file.write("myData = [\n")  # start the JavaScript array

## Step 4: Process each location row
record_count = 0  # to count how many valid records are processed

for location_row in db_cursor:
    geodata_bytes = location_row[1]  # the second column contains JSON data as bytes
    geodata_str = str(geodata_bytes.decode())  # decode to a UTF-8 string

    try:
        json_data = json.loads(geodata_str)  # parse JSON string into a Python dictionary
    except:
        continue  # skip invalid JSON rows

    if len(json_data['features']) == 0:
        continue  # skip rows with no location data

    try:
        latitude = json_data['features'][0]['geometry']['coordinates'][1]
        longitude = json_data['features'][0]['geometry']['coordinates'][0]
        place_name = json_data['features'][0]['properties']['display_name']
        place_name = place_name.replace("'", "")  # sanitize single quotes
    except:
        print('Unexpected format')
        print(geodata_str)
        continue  # skip improperly structured records

    try:
        print(place_name, latitude, longitude)  # show what's being processed

        record_count += 1
        if record_count > 1:
            output_file.write(",\n")  # add comma/newline for all but the first entry
        js_array_entry = f"[{latitude}, {longitude}, '{place_name}']"
        output_file.write(js_array_entry)
    except:
        continue  # skip entries that fail formatting/writing

## Step 5: Finalize and close everything
output_file.write("\n];\n")  # close the JavaScript array
db_cursor.close()  # close the cursor
output_file.close()  # close the JS file

print(record_count, "records written to where.js")  # summary
print("Open where.html to view the data in a browser")  # next step