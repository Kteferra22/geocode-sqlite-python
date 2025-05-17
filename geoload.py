## STEP 1 : Set up import functions

import urllib.request, urllib.parse, urllib.error #access the web and read url, build urls with query parameters, handles errors
import http #gives access to lower-level HTTP protocol details
import sqlite3 #lets you create and manage a local SQLite database
import json #allows you to work with JSON data, which is what the geolocation API returns. Takes raw text from the web and turns it into a usable python dictionary
import time #lets you pause the program for a few seconds using time.sleep()
import ssl #handles SSL certifications(secure web connection) and ignores SSL errors, so program won't crash

## STEP 2 : Set up the API Endpoints

serviceurl = 'https://py4e-data.dr-chuck.net/opengeo?' #defines the base URL for the geolocation API being called, ? at the end means we will be adding parameters later
# https://py4e-data.dr-chuck.net/opengeo?q=Ann+Arbor%2C+MI ##example of starting point with serviceurl and ? that adds specifc parameter (urlencode(parms)), which is the actual location needing to be found 

## STEP 3 : Open/create the database and prepare to use it
database_connection = sqlite3.connect('opengeo.sqlite') #connects to SQLite database and creates a new database of not already made named(opengeo.sqlite)
database_cursor = database_connection.cursor() #creates cursor or hand uses to execute SQL commands like queries, inserts, and table creation(like a remote control interacting with the database)
database_cursor.execute('''
CREATE TABLE IF NOT EXISTS Locations (address TEXT, geodata TEXT)''') #creates a table called Locations if it doesn't exist. Table has 2 columns, address(to store location strings) and geodata(to store the JSON geodata from the API)

## STEP 4 : Set up SSL context 
ssl_context = ssl.create_default_context() #creates a secure context that ignores SSL certificate errors
ssl_context.check_hostname = False #allows the program to connect to HTTPS URLs even if their SSL certificates are invalid or untrusted
ssl_context.verify_mode = ssl.CERT_NONE #important to avoid erros when making web requests

## STEP 5 : open the input file and initialize counters
input_file = open("where.data") #reads the file to be ready to be processed, given a variable name
processed_count = 0 #counter for how many locations processed 
not_found_count = 0 #counter for locations not found by the API

## STEP 6 : Loop through addresses and check cache
for address_line in input_file: #starts loop to read each line, line by line
    if processed_count > 100 : #if processed more than 100 addresses, stop the loop(prvents overloading the API or program)
        print('Retrieved 100 locations, restart to retrieve more')
        break 

    address = address_line.strip() #removes any extra spaces or newline characters from the addresses
    print('') #seperates information from line above with a space in between for clarity(like pressing the enter key)
    database_cursor.execute("SELECT geodata FROM Locations WHERE address= ?", #asks if the address is aleady stored, if not store it
        (memoryview(address.encode()),)) #changes Unicode the data in python into UTF8 bytes because it moving over to SQLite database
    try:
        data = database_cursor.fetchone()[0] #if address is found in line as sub 0, print its found, if not pass onto the next line 
        print("Found in database", address)
        continue
    except:
        pass

## STEP 7 : Get data from the API and save it      
    request_parameters = dict() #creates an empty dictionary(a box for storing data as key-value pairs)
    request_parameters['q'] = address #put addresses inside paramters box with the label 'q' and it will be sent to the website to ask about that address. 

    full_url = serviceurl + urllib.parse.urlencode(request_parameters)
    print('Retrieving', full_url) #prints the URL being used

    web_response = urllib.request.urlopen(full_url, context=ssl_context) #opens the URL and reads the data returned
    raw_data = web_response.read().decode() #decodes it from Unicode to readble text for the website UTF8
    
    print('Retrieved', len(raw_data), 'characters', raw_data[:20].replace('\n', ' ')) #how many characters were recieved in the data(len(data)), the first 20 characters (data[:20]), and also replaces any line breaks (\n) in those first 20 characters with a space, so it looks cleaner
    
    processed_count = processed_count + 1 #adds 1 to the number of addresses processed 

    try:
        json_data = json.loads(raw_data) #attempts to change the data into a JSON format thats easy to work with in Python
    except:
        print(raw_data) #if it fails prints raw data and moves on to the next address
        continue

    if not json_data or 'features' not in json_data: #if the json data does not some with features it cannnot process the data(like asking for directions and not getting an answer)
        print('==== Download error ===') #if not, it prints an error and stops the program prints data then stops the program to find out what went wrong
        print(raw_data)
        break

    if len(json_data['features']) == 0: #same as previous, if no features in data retrieval, meaning the features list is empty, that means no location was found
        print('==== Object not found ====') #prints message 
        not_found_count = not_found_count + 1 #counts the address as a missing location

    database_cursor.execute('''INSERT INTO Locations (address, geodata)
        VALUES ( ?, ? )''', #enters new data into the address and geodata column 
        (memoryview(address.encode()), memoryview(raw_data.encode()) ) ) #converts Unicode string from python to UTF8 bytes because it going into SQLite Database 

    database_connection.commit() #saves these changes permanently in the database

    if processed_count % 10 == 0 : #if the count is divisible by 10 meaning 10/10 or 20/10 is a whole number and there is no remainder(%)
        print('Pausing for a bit...') #if thats the case print pausing for a bit(sleeps for 5 seconds to prvent overloading the web server by sending too many requsts too quickly)
        time.sleep(5)

if not_found_count > 0: #prints how many addresses were not found 
    print('Number of features for which the location could not be found:', not_found_count)

print("Run geodump.py to read the data from the database so you can vizualize it on a map.") #after running this script and it saves the location data, run the next program(geodump.py) that will use this saved data to show the locations on a map

