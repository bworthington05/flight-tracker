import sqlite3
"""
This module contains functions for looking up info about an aircraft using its
mode S code/hex ID. The SQLite queries here assume that the aircraft database
was setup with faa_data_loader.py script.
"""

def get_aircraft_type(database, mode_s_code_hex):
	"""
	Looks up an aircraft's type based on the mode_s_code_hex in the FAA's database.  
	Example: BOEING 747-47UF or A319-132

	Parameters:
		1 - database file path
		2 - mode_s_code_hex (must be all uppercase string)

	Returns:
		The aircraft's type
	"""

	# Some lines of code are commented out because this function was originally written
	# to return an aicraft's manufacturer + model, but now it just returns the model.
	# The plan is to add a function that specifically returns manufacturer later.

	# Connect to the database
	conn = sqlite3.connect(database)

	select_statement = (
		'SELECT '
			#'IFNULL(faa_acftref.mfr, "MFR?"), '
			'IFNULL(faa_acftref.model, "MODEL?") '
		'FROM faa_master '
			'LEFT OUTER JOIN faa_acftref ON faa_master.mfr_mdl_code = faa_acftref.code '
		'WHERE faa_master.mode_s_code_hex LIKE "' + mode_s_code_hex + '%";')

	results = conn.execute(select_statement)

	# Get the one and only row of the results set
	result = results.fetchone()

	conn.close()

	# In the event that no results at all are returned
	if result is not None:
		# Create strings of manufacturer & model with trailing whitespace removed
		#mfr = str(result[0]).rstrip()
		model = str(result[0]).rstrip()

	else:
		#mfr = "MFR?"
		model = "MODEL?"

	#aircraft_type = mfr + " " + model

	#return aircraft_type
	return model


def get_aircraft_registrant(database, mode_s_code_hex):
	"""
	Looks up an aircraft's registrant's name based on the mode_s_code_hex
	in the FAA's database.  Example: FEDERAL EXPRESS CORP (a FedEx plane)

	Parameters:
		1 - database file path
		2 - mode_s_code_hex (must be all uppercase string)

	Returns:
		The aircraft's registrant
	"""

	# Connect to the database
	conn = sqlite3.connect(database)

	select_statement = (
		'SELECT '
			'IFNULL(faa_master.name, "REG?") '
		'FROM faa_master '
		'WHERE faa_master.mode_s_code_hex LIKE "' + mode_s_code_hex + '%";')

	results = conn.execute(select_statement)

	# Get the one and only row of the results set
	result = results.fetchone()

	conn.close()

	# In the event that no results at all are returned
	if result is not None:
		# Create string of registrant name with trailing whitespace removed
		registrant = str(result[0]).rstrip()

	else:
		registrant = "REG?"

	return registrant
