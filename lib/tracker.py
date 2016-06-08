import requests
import json
from aircraft import *
import transponder_message_example
import datetime

class Tracker:

	def __init__(self, database):
		"""
		Constructor to create a new Tracker object.
		Aircraft are created, updated, and tracked as Aircraft objects in a list.

		Parameters:
			1 - FAA database file path (used when creating Aircraft objects)
		"""

		self.database = database
		self.seen_limit = 60  # Max limit for the "seen" element of a message before aircraft is removed from list
		self.aircraft_list = []  # List that will hold Aircraft objects being tracked

		# These are updated everytime get_flights() is called
		self.number_updated = 0
		self.number_created = 0
		self.number_messages_received = 0

		# Indicator if there was a connection error, can be used to display a waring in the GUI
		self.connection_error = False

		# Variable for recording the exact time when the tracker updates
		self.current_time = datetime.datetime.now().time()


	def get_flights(self, url):
		"""
		This function receives data (in JSON format) being broadcast by aircraft via their Mode S transponders.
		It checks if each aircraft is currently being "tracked" in the provided aircraft list.
		If not, it creates a new Aircraft object and adds it to the list.
		If the airtcraft is already in the list, its instance variables are updated with info from the new message.

		Parameters:
			1 - the URL to connect with (in the format http://[IP address]:8080/data.json)
		"""

		self.current_time = datetime.datetime.now().time()

		# Holding bin for JSON formatted results (transponder messages) returned from request.get()
		# Intialized as an empty list so that the "if len(json_data) > 0" statement after the try/except block
		# will still work even if there was a connection error 
		json_data = []

		try:
			response = requests.get(url)
			raw_text = response.text
			json_data = json.loads(raw_text)
			self.connection_error = False

		except requests.ConnectionError:
			self.connection_error = True

		# Uncomment the statement below to load in sample data for testing purposes
		# json_data = json.loads(transponder_message_example.test_message)

		# Reset these to 0 each time this function is called
		self.number_updated = 0
		self.number_created = 0
		self.number_removed = 0

		self.number_messages_received = len(json_data)
		
		# If request actually returns results
		if len(json_data) > 0:
			
			for message in json_data:
				hex_code = str(message.get('hex')).upper()
				in_list = False

				# Check if hex code belongs to an aircraft that is already in the list
				# by looping through each aircraft
				for aircraft in self.aircraft_list:

					# If the if the aircraft is in the list...
					if hex_code == aircraft.hex_code:

						# Check if its last message is over the seen_limit
						# and if so, remove the aircraft from the list
						if aircraft.seen > self.seen_limit:
							self.aircraft_list.remove(aircraft)
							self.number_removed += 1
							break

						# Otherwise, update its info based on the current message
						else:
							aircraft.update_info(message)
							in_list = True
							self.number_updated += 1
							break

				# If it's not in the list, create a new Aircraft object and append it to the list
				# but only if its last message isn't over the seen_limit
				if not in_list and message.get('seen') <= self.seen_limit:
					self.aircraft_list.append(Aircraft(message, self.database))
					self.number_created += 1


	def clear_list(self):
		"""
		Makes the aircraft_list empty.  
		May be useful if the list needs to be reset from the GUI in the event that
		the connection is broken.
		"""
		self.aircraft_list = []


	def summary_headings(self):
		"""
		Returns a string with headings to match the columns in the string returned
		by Aircraft's summary function.

		Parameters:
			None
		"""

		summary_headings = (
			'HEX'.ljust(6) + '  ' +
			'FLT'.ljust(8) + '  ' +
			'ALT'.ljust(6) + '  ' +
			'LAT'.ljust(10) + '  ' +
			'LON'.ljust(10) + '  ' +
			'SPD'.ljust(4) + '  ' +
			'TRK'.ljust(3) + '  ' +
			'SEC'.ljust(3) + '  ' +
			'TYPE'.ljust(20)
		)

		return summary_headings