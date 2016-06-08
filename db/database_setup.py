import numpy
import sqlite3
"""
This module contains functions for setting up a database (creating tables, inserting data, etc.).
"""

def create_table(database, table, headers):
    """
    This function creates a SQLite table.

    Parameters:
        1 - string file path of database (if the database doesn't exist, it will be created)
        2 - string name of the table being created
        3 - list of headers/field names/column names that the table will store
    """
    
    # This variable will be a string of field names used to make the SQLite create table statement
    fields_for_create = ''
    
    n = 0
    
    while n < len(headers):
        
        fields_for_create += headers[n] + ' TEXT'  # Indicate that each field will store text values
            
        if n < (len(headers) - 1):  # Add commas after every value except the last one
            fields_for_create += ','
            
        n += 1
    
    create_statement = ('''CREATE TABLE IF NOT EXISTS ''' + table + '''(''' + fields_for_create + ''')''')
    
    # Connect to the specified database
    con = sqlite3.connect(database)
    cursor = con.cursor()
    
    # Create the table using the create_statement from above
    cursor.execute(create_statement)
    con.commit()
    
    print "the " + table + " table was successfully created or it already exists\n"
    
    con.close()
    

def insert_data(database, table, data):
    """
    This function inserts data into an existing table of a SQLite database.

    Parameters:
        1 - string file path of database (if the database doesn't exist, it will be created)
        2 - string name of the table the data is going into
        3 - the dataset, which must be an array of tuples (each record is a tuple), and the first tuple must
            include the field names of the table
    """
    
    # Pop off the first row of the dataset and save it as the headers
    headers = data.pop(0)
    
    fields_for_insert = ''
    question_marks = ''
    
    n = 0
    
    while n < len(headers):
        
        fields_for_insert += headers[n]
        question_marks += '?'
            
        if n < (len(headers) - 1):  # Add commas after every value except the last one
            fields_for_insert += ','
            question_marks += ','
            
        n += 1
    
    insert_statement = ('''INSERT INTO ''' + table + '''(''' + fields_for_insert + ''') VALUES(''' + question_marks + ''')''')
    
    # Connect to the specified database
    con = sqlite3.connect(database)
    cursor = con.cursor()
    
    # Insert data into the table using the insert_statement from above and supplied dataset
    cursor.executemany(insert_statement, data)
    con.commit()
    
    print 'inserted ' + str(len(data)) + ' records into ' + table + ' table\n'
    
    con.close()


def create_table_and_insert(database, table, data):
    """
    This function creates a table in a SQLite databse AND inserts data into that table.
    If the table already exists, it is dropped first.

    Parameters:
        1 - string file path of database (if the database doesn't exist, it will be created)
        2 - string name of the table the data is going into
        3 - the dataset, which must be an array of tuples (each record is a tuple), and the first tuple must
            include the field names of the table
    """

    # Pop off the first row of the dataset and save it as the headers
    headers = data.pop(0)
    
    # These string variables will be concatenated with headers and used to make 
    # the SQLite create table and insert data statements
    fields_for_create = ''
    fields_for_insert = ''
    question_marks = ''
    
    n = 0
    
    while n < len(headers):
        
        fields_for_create += headers[n] + ' TEXT'
        fields_for_insert += headers[n]
        question_marks += '?'
            
        if n < (len(headers) - 1):  # Add commas after every value except the last one
            fields_for_create += ','
            fields_for_insert += ','
            question_marks += ','
            
        n += 1
    
    create_statement = ('''CREATE TABLE ''' + table + '''(''' + fields_for_create + ''')''')
    
    insert_statement = ('''INSERT INTO ''' + table + '''(''' + fields_for_insert + ''') VALUES(''' + question_marks + ''')''')
    
    # Connect to the specified database
    con = sqlite3.connect(database)
    cursor = con.cursor()
    
    # Drop table if it already exists so we can start fresh
    cursor.execute('''DROP TABLE IF EXISTS ''' + table)
    con.commit()
    
    # Create the table using the create_statement from above
    cursor.execute(create_statement)
    con.commit()
    print 'SQLite table created: ' + table
    
    # Insert data into the table using the insert_statement from above and supplied dataset
    cursor.executemany(insert_statement, data)
    con.commit()
    
    print 'inserted ' + str(len(data)) + ' records into ' + table + ' table\n'
    
    con.close()
    

def get_data_from_text_file(filename):
    """
    This function reads in data from a comma delimited .txt file.
    The first row of the file should be headers with column/field names.

    Parameters:
        1 - the string file path of the .txt file

    Returns:
        A multidimensional list of data in the .txt file
    """

    data = numpy.genfromtxt(filename, dtype=str, delimiter=',')

    # Convert numpy ndarray to a list so that functions like pop() and remove() can be used
    data = data.tolist()

    print filename + ' loaded successfully, ' + str(len(data) - 1) + ' records retrieved\n'

    return data

    