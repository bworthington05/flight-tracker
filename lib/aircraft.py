import aircraft_lookup
"""
This module contains a class that represents an Aircraft object. There is a constructor
to create a new Aircraft and a function to update the information about that Aircraft.
"""

class Aircraft:

	def __init__(self, message, database):
		"""
		Constructor to create a new Aircraft object.

		Parameters:
			1 - message received from Mode S transponder in JSON format
			2 - file path of database containing FAA's aircraft registration info
		"""

		# Get whatever data is being broadcast by the aircraft's Mode S transponder
		self.hex_code = str(message.get('hex')).upper()
		self.flight = str(message.get('flight'))
		if len(self.flight) == 0:
			self.flight = 'N/A'

		self.validposition = message.get('validposition')
		self.lat = message.get('lat')
		self.lon = message.get('lon')
		if self.validposition == 0:
			self.lat = 'N/A'
			self.lon = 'N/A'

		self.altitude = message.get('altitude')
		self.validtrack = message.get('validtrack')
		self.track = message.get('track')
		if self.validtrack ==0:
			self.track = 'N/A'

		self.speed = message.get('speed')
		self.messages = message.get('messages')
		self.seen = message.get('seen')

		# Use the aircraft's hex code to identify its registrant and type based on FAA database
		# self.aircraft_reg = aircraft_lookup.get_aircraft_registrant(database, self.hex_code)
		self.aircraft_type = aircraft_lookup.get_aircraft_type(database, self.hex_code)


	def update_info(self, message):
		"""
		Update the Aircraft object's info based on newly received data from its Mode S transponder.
		Some of the object's instance variables will be updated, but not all. For example, no reason to
		update the hex_code or check again for type and registrant in FAA database.

		Parameters:
			1 - message received from Mode S transponder in JSON format
		"""

		self.flight = str(message.get('flight'))
		if len(self.flight) == 0:
			self.flight = 'N/A'

		self.validposition = message.get('validposition')
		self.lat = message.get('lat')
		self.lon = message.get('lon')
		if self.validposition == 0:
			self.lat = 'N/A'
			self.lon = 'N/A'

		self.altitude = message.get('altitude')
		self.validtrack = message.get('validtrack')
		self.track = message.get('track')
		if self.validtrack ==0:
			self.track = 'N/A'
			
		self.speed = message.get('speed')
		self.messages = message.get('messages')
		self.seen = message.get('seen')


	def summary(self):
		"""
		Creates a formatted string describing the current state of this aircraft.
		The string is formatted to fit on one line and have columns start at the same position.

		Parameters:
			None

		Returns:
			String description of aircraft
		"""

		# For each instance variable, convert to a string, then make sure it's not longer than x charcters
		# then use ljust() or rjust() to pad with extra spaces if shorter than x characters
		summary = (
			(str(self.hex_code)[:6]).ljust(6) + '  ' +
			(str(self.flight)[:8]).ljust(8) + '  ' +
			(str(self.altitude)[:6]).ljust(6) + '  ' +
			(str(self.lat)[:10]).ljust(10) + '  ' +
			(str(self.lon)[:10]).ljust(10) + '  ' +
			(str(self.speed)[:4]).ljust(4) + '  ' +
			(str(self.track)[:3]).ljust(3) + '  ' +
			(str(self.seen)[:3]).ljust(3) + '  ' +
			(str(self.aircraft_type)[:30]).ljust(20)
		)

		return summary
