from math import radians, sin, cos, sqrt, atan2, degrees
import decimal
"""
This module contains functions to perform calculations on latitude and longitude coordinates.
"""

def get_distance(lat1, lon1, lat2, lon2, unit='miles'):
	"""
	Calculate the distance between two points on Earth given their latitude and
	longitude as decimal degrees. Caculations are done using the haversine formula.

	http://www.igismap.com/haversine-formula-calculate-geographic-distance-earth/
	https://en.wikipedia.org/wiki/Haversine_formula
	https://rosettacode.org/wiki/Haversine_formula

	Parameters:
		1 - latitude of position 1
		2 - longitude of position 1
		3 - latitude of position 2
		4 - longitude of position 2
		5 - unit of distance (optional), "miles" or "km", default is miles

	Returns:
		The distance in whatever unit is specified as a parameter (miles or kilometers)
	"""

	# First set the value of Earth's radius based on desired unit for measuring distance
	if unit == 'miles':
		earth_radius = 3959  # radius in miles

	elif unit == 'km':
		earth_radius = 6371  # radius in kilometers

	else:
		print '\nunknown units: ' + str(unit) + '\n'

	# Convert latitude and longitude degrees to radians
	dif_lat = radians(lat2 - lat1)
	dif_lon = radians(lon2 - lon1)
	lat1 = radians(lat1)
	lat2 = radians(lat2)

	a = (sin(dif_lat / 2)**2) + cos(lat1) * cos(lat2) * (sin(dif_lon / 2)**2)

	c = 2 * atan2(sqrt(a), sqrt(1-a))

	distance = earth_radius * c

	return distance


def get_bearing(lat1, lon1, lat2, lon2):
	"""
	Calculate the bearing of point 2 relative to point 1 given their latitude and
	longitude as decimal degrees.

	http://www.igismap.com/formula-to-find-bearing-or-heading-angle-between-two-points-latitude-longitude/

	Parameters:
		1 - latitude of position 1
		2 - longitude of position 1
		3 - latitude of position 2
		4 - longitude of position 2

	Returns:
		The bearing in degrees
	"""

	# Convert latitude and longitude degrees to radians
	lat1 = radians(lat1)
	lat2 = radians(lat2)
	dif_lon = radians(lon2 - lon1)

	x = cos(lat2) * sin(dif_lon)
	y = cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(dif_lon)

	bearing = atan2(x, y)
	bearing = degrees(bearing)
	bearing = (bearing + 360) % 360
	
	return bearing


def get_scale(lat1, lon1, var, desired_distance, unit='miles'):
	"""
	Calculate the difference in either latitude or longitude that is equivalent
	to some desired distance at a given point on Earth.  For example, at a specific 
	point, how much does latitude need to change (assuming longitude is constant) to
	be equal to 60 miles?  This is especially important since lines of longitude are
	closer together near Earth's poles.  This function is helpful when converting
	latitude and longitude coordinates to pixel coordinates in order to plot a point
	on the screen.

	Parameters:
		1 - latitude of position in decimal degrees
		2 - longitude of position in decimal degrees
		3 - "lat" or "lon" to specify if calulating change for latitude or longitude
		4 - the desired distance from the given point
		5 - unit of measure (optional), "miles" or "km", default is miles

	Returns:
		The difference in latitude or longitude
	"""

	# Create a second point that is initially set to the starting point
	# The idea is to that push this point farther and farther away (either by lat or lon)
	# until it is the desired distance away
	lat2 = lat1
	lon2 = lon1

	# Create a variable for tracking the actual distance between the two points, which
	# can be compared against the desired distance
	actual_distance = get_distance(lat1, lon1, lat2, lon2, unit)

	n = 1  # Place value to increase or decrease lat/lon by (1, .1, .01, .001, etc.)

	decrease_n = False  # Flag to indicate if n should be decreased

	if var == 'lat':
		var_value = lat2  # Variable for holding either latitude or longitude (whichever is being modified)

	elif var == 'lon':
		var_value = lon2

	else:
		print '\nvalue not recognized: ' + str(var)  + '\n'

	# Keep looping until the difference between the desired distance and the actual distance
	# is less than 0.0001 (in whatever units)... basically until it's really close
	while abs(round(desired_distance - actual_distance, 4)) > 0.0001:

		# Keep increasing the var_value until the actual distance is too great, then start decreasing until it's too small

		# If desired distance is greater than actual, add n to the var_value
		if desired_distance > actual_distance:

			var_value += n
			var_value = round(var_value, 6)  # Round to 6 decimal places to clean up floating point messiness

			decrease_n = True  # Indicate it's ok the decrease n if the following else statement is evaluated

		# If actual distance is greater than desired, subtract n from var_value
		else:

			if decrease_n:
				n *= 0.1  # Decrease n by a factor of ten

			var_value -= n
			var_value = round(var_value, 6)

			decrease_n = False  # Don't decrease n until after the next time the if statement is evaluated

		# Recalculate the actual distance
		if var == 'lat':
			actual_distance = get_distance(lat1, lon1, var_value, lon2, unit)

		else:
			actual_distance = get_distance(lat1, lon1, lat2, var_value, unit)

		# print round(actual_distance, 4)  for testing purposes

	# Return the difference between lat2 and lat1 (or lon2/lon1) that is equal to the desired distance
	if var == 'lat':
		return abs(round(var_value - lat1, 6))

	else:
		return abs(round(var_value - lon1, 6))
