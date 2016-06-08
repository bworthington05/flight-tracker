import database_setup
"""
Load data from FAA aircraft database .txt files to a SQLite database.
http://www.faa.gov/licenses_certificates/aircraft_certification/aircraft_registry/releasable_aircraft_download/

FAA .txt files require a little prep work before they can be loaded:
1. Add a field/column header after the last comma called "BLANK" since every row ends with a comma
2. Replace every hyphen in the column headers with underscores
3. Find and replace hashtags with some other character (causes an error when saving to SQLite database)
4. Convert the file to UTF-8 encoding instead of UTF-8-BOM

Uses the database_setup module.
"""
# SQLite database where the .txt file data should be loaded into
database = 'faa_database.db'

#########################
# Load FAA ACFTREF data #
#########################

table = 'faa_acftref'
file = 'text_files/acftref.txt'

# Get data from the .txt file
data = database_setup.get_data_from_text_file(file)

# Display some of the data to make sure it looks right
print table + ' headers:'
print data[0]

print '\n'

print table + ' row 1:'
print data[1]

print '\n'

# Create a table in the database and save this dataset
database_setup.create_table_and_insert(database, table, data)

########################
# Load FAA MASTER data #
########################

table = 'faa_master'
file = 'text_files/master.txt'

data = database_setup.get_data_from_text_file(file)

print table + ' headers:'
print data[0]

print '\n'

print table + ' row 1:'
print data[1]

print '\n'

database_setup.create_table_and_insert(database, table, data)

    