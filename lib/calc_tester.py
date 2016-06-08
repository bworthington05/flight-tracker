import calculations

lat2 = 30.033706
lon2 = -90.053415

lat1 = 30.413940
lon1 = -90.397338

unit = 'miles'

distance = calculations.get_distance(lat1, lon1, lat2, lon2, unit)
bearing = calculations.get_bearing(lat1, lon1, lat2, lon2)

print 'distance between points 1 & 2: ' + str(round(distance)) + ' ' + unit
print 'bearing of point 2: ' + str(round(bearing))


