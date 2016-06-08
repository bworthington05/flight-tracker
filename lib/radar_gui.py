from Tkinter import *
from tracker import *
import time
import calculations
import radar_config

class GUI:

	def __init__(self):

		########################################
		# Load default values from config file #
		########################################

		# Latitude and longitude of the point at the center of the radar display
		self.current_lat = radar_config.DEFAULT_LAT
		self.current_lon = radar_config.DEFAULT_LON

		# IP address to ping in order to receive transponder messages
		self.ip_address = radar_config.DEFAULT_IP

		# Variables that will hold the scale used to convert between lat/lon and pixel coordinates
		self.lat_scale = None
		self.lon_scale = None

		self.unit_of_distance = radar_config.DEFAULT_UNIT_OF_DISTANCE

		# File path of the FAA database that contains info about planes linked to transponder hex ID
		self.database = radar_config.DATABASE

		# Create the Tracker object that parses transponder messages, maintains a list of aircraft being tracked
		# and creates/updates data for each aircraft being tracked
		self.tracker = Tracker(self.database)

		#########################################
		# Create the main containers / displays #
		#########################################

		# Master/root container
		self.master = Tk()
		self.master.bind_all("<1>", lambda event:event.widget.focus_set())

		# Create the main container for organizing other widgets
		self.main_container = Frame(self.master)
		self.main_container.pack()

		# Create the flight data display
		self.data_display_containter = Frame(self.main_container)
		self.data_display_containter.pack(side=LEFT, anchor=NW, padx=5, pady=5)

		# Create the radar screen display
		self.radar_screen = Canvas(self.main_container, width=600, height=600, bg='black', highlightthickness=0)
		self.radar_screen.pack(side=LEFT, anchor=NW, pady=5)

		# Create the container for smaller containers of buttons related to the radar display
		self.button_container = Frame(self.main_container)
		self.button_container.pack(side=LEFT, anchor=NW, padx=5, pady=5)

		############################################
		# Import symbols used by the radar display #
		############################################

		self.green_square = PhotoImage(file='radar_graphics/green_square.gif')
		self.red_square = PhotoImage(file='radar_graphics/red_square.gif')

		##############################################################
		# Checkbuttons that control radar display formatting options #
		##############################################################

		self.radar_show_container = Frame(self.button_container)
		self.radar_show_container.pack(side=TOP, pady=10)

		self.radar_show_var_grid = IntVar()
		self.radar_show_var_crosshairs = IntVar()
		self.radar_show_var_circles = IntVar()
		self.radar_show_var_degrees = IntVar()
		self.radar_show_var_range = IntVar()

		self.radar_show_label = Label(self.radar_show_container, text='DISPLAY OPTIONS', width=20)
		self.radar_show_grid = Checkbutton(self.radar_show_container, text='GRID', variable=self.radar_show_var_grid)
		self.radar_show_crosshairs = Checkbutton(self.radar_show_container, text='CROSSHAIRS', variable=self.radar_show_var_crosshairs)
		self.radar_show_circles = Checkbutton(self.radar_show_container, text='CIRCLES', variable=self.radar_show_var_circles)
		self.radar_show_degrees = Checkbutton(self.radar_show_container, text='DEGREES', variable=self.radar_show_var_degrees)
		self.radar_show_range = Checkbutton(self.radar_show_container, text='RANGE', variable=self.radar_show_var_range)

		self.radar_show_label.pack(anchor=NW)
		self.radar_show_grid.pack(anchor=NW)
		self.radar_show_crosshairs.pack(anchor=NW)
		self.radar_show_circles.pack(anchor=NW)
		self.radar_show_degrees.pack(anchor=NW)
		self.radar_show_range.pack(anchor=NW)

		# Select some checkbuttons for features to initially display on the radar screen
		self.radar_show_crosshairs.select()
		self.radar_show_circles.select()
		self.radar_show_degrees.select()
		self.radar_show_range.select()

		#########################################################
		# Radiobuttons that control radar display range options #
		#########################################################

		self.range_container = Frame(self.button_container)
		self.range_container.pack(side=TOP, pady=10)

		# Variable to indicate what the unit of distance should be when performing calculations and for the radar display
		self.range_unit = IntVar()

		# Variable to hold the range of the radar display
		self.range = IntVar()

		# Radiobuttons for unit of distance
		self.range_unit_km = Radiobutton(self.range_container, text='KM', variable=self.range_unit, value=1, command=self.update_unit_of_distance)
		self.range_unit_miles = Radiobutton(self.range_container, text='MILES', variable=self.range_unit, value=2, command=self.update_unit_of_distance)        

		# Radiobutttons for radar display range options: short = 15 miles, medium = 30 miles, long = 60 miles
		self.range_label = Label(self.range_container, text='RANGE/UNIT OPTIONS', width=20)
		self.range_short = Radiobutton(self.range_container, text='SHORT', variable=self.range, value=15, command=self.update_scale)
		self.range_medium = Radiobutton(self.range_container, text='MEDIUM', variable=self.range, value=30, command=self.update_scale)
		self.range_long = Radiobutton(self.range_container, text='LONG', variable=self.range, value=60, command=self.update_scale)
		self.range_vlong = Radiobutton(self.range_container, text='VERY LONG', variable=self.range, value=120, command=self.update_scale)

		self.range_label.pack(anchor=NW)
		self.range_unit_km.pack(anchor=NW)
		self.range_unit_miles.pack(anchor=NW)
		self.range_short.pack(anchor=NW)
		self.range_medium.pack(anchor=NW)
		self.range_long.pack(anchor=NW)
		self.range_vlong.pack(anchor=NW)

		# Select the default range and units
		self.range_unit_miles.select()
		self.range_long.select()

		# Set the initial scale based on the defaul range radiobutton selected
		self.update_scale()

		############################################################
		# Buttons and entry fields that control network connection #
		############################################################

		self.conn_container = Frame(self.button_container)
		self.conn_container.pack(side=TOP, pady=10)

		# Variable to indicate which connection button is select (on/off)
		self.conn_status = IntVar()

		self.conn_label = Label(self.conn_container, text='CONNECTION', width=15)

		self.conn_ip_label = Label(self.conn_container, text='IP ADDRESS')
		self.conn_status_label = Label(self.conn_container, text='STATUS')

		self.conn_ip_entry = Entry(self.conn_container, width=9)
		self.conn_ip_entry.insert(0, self.ip_address)

		# Update the ip_address when user presses Enter key after typing into the conn_ip_entry field
		self.conn_ip_entry.bind("<Return>", self.update_ip_address)

		self.conn_status_indicator = Label(self.conn_container, text='UNKN', bg='yellow', width=7)

		self.conn_on = Radiobutton(self.conn_container, text='ON', variable=self.conn_status, value=1, width=7, indicatoron=0)
		self.conn_off = Radiobutton(self.conn_container, text='OFF', variable=self.conn_status, value=0, width=7, indicatoron=0)

		# Initial setting to have connection turned off
		self.conn_off.select()

		self.conn_label.grid(row=0, columnspan=4)
		self.conn_ip_label.grid(row=1, column=0, columnspan=2, padx=5, sticky=W)
		self.conn_status_label.grid(row=1, column=2, columnspan=2, padx=5, sticky=W)
		self.conn_ip_entry.grid(row=2, column=0, columnspan=2, padx=5, sticky=W)
		self.conn_status_indicator.grid(row=2, column=2, columnspan=2, padx=5, sticky=W)
		self.conn_on.grid(row=3, column=0, columnspan=2, pady=5, padx=5, sticky=W)
		self.conn_off.grid(row=3, column=2, columnspan=2, pady=5, padx=5, sticky=W)

		#######################################################################
		# Buttons and entry fields that uptdate center latitude and longitude #
		#######################################################################

		self.latlon_container = Frame(self.button_container)
		self.latlon_container.pack(side=TOP, pady=10)

		self.latlon_label = Label(self.latlon_container, text='CENTER POSITION', width=15)

		self.lat_label = Label(self.latlon_container, text='LATITUDE')
		self.lon_label = Label(self.latlon_container, text='LONGITUDE')

		# Entry fields for lat and lon, display default lat and lon to start
		self.lat_entry = Entry(self.latlon_container, width=10)
		self.lat_entry.insert(0, self.current_lat)

		self.lon_entry = Entry(self.latlon_container, width=10)
		self.lon_entry.insert(0, self.current_lon)

		# Button that updates values for current_lat and current_lon based on what is in the entry fields above
		self.latlon_update_button = Button(self.latlon_container, text='UPDATE', width=7, command=self.update_latlon)
		self.latlon_reset_button = Button(self.latlon_container, text='RESET', width=7, command=self.reset_latlon)

		self.latlon_label.grid(row=0, columnspan=4)
		self.lat_label.grid(row=1, column=0, columnspan=2, padx=5, sticky=W)
		self.lon_label.grid(row=1, column=2, columnspan=2, padx=5, sticky=W)
		self.lat_entry.grid(row=2, column=0, columnspan=2, padx=5, sticky=W)
		self.lon_entry.grid(row=2, column=2, columnspan=2, padx=5, sticky=W)
		self.latlon_update_button.grid(row=3, column=0, columnspan=2, pady=5, padx=5, sticky=W)
		self.latlon_reset_button.grid(row=3, column=2, columnspan=2, pady=5, padx=5, sticky=W)

		################################
		# Aircraft data summary screen #
		################################

		self.aircraft_summary_screen = Canvas(self.data_display_containter, width=480, height=350, bg='black', highlightthickness=0, scrollregion=(0,0,700,700))
		self.aircraft_summary_screen.grid(row=0, columnspan=3)

		self.summary_x_scrollbar = Scrollbar(self.data_display_containter, orient=HORIZONTAL, command=self.aircraft_summary_screen.xview)
		self.summary_x_scrollbar.grid(row=1, column=0, columnspan=3, sticky=W+E)

		self.summary_y_scrollbar = Scrollbar(self.data_display_containter, orient=VERTICAL, command=self.aircraft_summary_screen.yview)
		self.summary_y_scrollbar.grid(row=0, column=2, sticky=E+N+S)

		self.aircraft_summary_screen.config(xscrollcommand=self.summary_x_scrollbar.set, yscrollcommand=self.summary_y_scrollbar.set)

		#########################
		# Aircraft list options #
		#########################

		self.aircraft_tracking_container1 = Frame(self.data_display_containter)
		self.aircraft_tracking_container1.grid(row=3, column=0, sticky=NW, padx=10, pady=20)

		self.list_label = Label(self.aircraft_tracking_container1, text='LIST OPTIONS')

		# Reset the aircraft list to be totally empty- helpful if the connection is broken and then old aircraft aren't being cleared
		self.list_reset_button = Button(self.aircraft_tracking_container1, text='RESET LIST', command=self.tracker.clear_list)

		# Variables and checkbuttons that filter the aircraft list being displayed in the summary screen
		self.list_var_position = IntVar()
		self.list_var_flight = IntVar()

		self.list_options_label = Label(self.aircraft_tracking_container1, text='\nONLY SHOW AIRCRAFT WITH:')
		self.list_only_position = Checkbutton(self.aircraft_tracking_container1, text='VALID POSITION', variable=self.list_var_position)
		self.list_only_flight = Checkbutton(self.aircraft_tracking_container1, text='FLIGHT NUMBER', variable=self.list_var_flight)
		
		self.list_label.grid(row=0, sticky=W)
		self.list_reset_button.grid(row=1, sticky=W)
		self.list_options_label.grid(row=2, sticky=W)
		self.list_only_position.grid(row=3, sticky=W)
		self.list_only_flight.grid(row=4, sticky=W)

		######################################
		# Aircraft tracking/lock on controls #
		######################################

		self.aircraft_tracking_container2 = Frame(self.data_display_containter)
		self.aircraft_tracking_container2.grid(row=3, column=1, columnspan=2, pady=20)

		self.tracking_label = Label(self.aircraft_tracking_container2, text='AIRCRAFT TRACKING')

		self.tracking_hex1 = Label(self.aircraft_tracking_container2, text='HEX:')
		self.tracking_hex2 = Label(self.aircraft_tracking_container2, text='HEX:')
		self.tracking_hex3 = Label(self.aircraft_tracking_container2, text='HEX:')

		# Entry fields for the hex IDs of each aircraft to be locked
		self.tracking_entry1 = Entry(self.aircraft_tracking_container2, width=8)
		self.tracking_entry2 = Entry(self.aircraft_tracking_container2, width=8)
		self.tracking_entry3 = Entry(self.aircraft_tracking_container2, width=8)

		self.tracking1 = IntVar()
		self.tracking2 = IntVar()
		self.tracking3 = IntVar()

		self.tracking_lock_button1 = Radiobutton(self.aircraft_tracking_container2, text='LOCK', width=8, variable=self.tracking1, value=1, indicatoron=0)
		self.tracking_unlock_button1 = Radiobutton(self.aircraft_tracking_container2, text='UNLOCK', width=8, variable=self.tracking1, value=0, indicatoron=0)
		self.tracking_unlock_button1.select()

		self.tracking_lock_button2 = Radiobutton(self.aircraft_tracking_container2, text='LOCK', width=8, variable=self.tracking2, value=1, indicatoron=0)
		self.tracking_unlock_button2 = Radiobutton(self.aircraft_tracking_container2, text='UNLOCK', width=8, variable=self.tracking2, value=0, indicatoron=0)
		self.tracking_unlock_button2.select()

		self.tracking_lock_button3 = Radiobutton(self.aircraft_tracking_container2, text='LOCK', width=8, variable=self.tracking3, value=1, indicatoron=0)
		self.tracking_unlock_button3 = Radiobutton(self.aircraft_tracking_container2, text='UNLOCK', width=8, variable=self.tracking3, value=0, indicatoron=0)
		self.tracking_unlock_button3.select()

		self.tracking_label.grid(row=0, columnspan=4)
		self.tracking_hex1.grid(row=1, column=0, sticky=W)
		self.tracking_entry1.grid(row=1, column=1, padx=10, pady=5, sticky=W)
		self.tracking_lock_button1.grid(row=1, column=2, padx=10, pady=5, sticky=W)
		self.tracking_unlock_button1.grid(row=1, column=3, padx=10, pady=5, sticky=W)

		self.tracking_hex2.grid(row=2, column=0, sticky=W)
		self.tracking_entry2.grid(row=2, column=1, padx=10, pady=5, sticky=W)
		self.tracking_lock_button2.grid(row=2, column=2, padx=10, pady=5, sticky=W)
		self.tracking_unlock_button2.grid(row=2, column=3, padx=10, pady=5, sticky=W)

		self.tracking_hex3.grid(row=3, column=0, sticky=W)
		self.tracking_entry3.grid(row=3, column=1, padx=10, pady=5, sticky=W)
		self.tracking_lock_button3.grid(row=3, column=2, padx=10, pady=5, sticky=W)
		self.tracking_unlock_button3.grid(row=3, column=3, padx=10, pady=5, sticky=W)

	def run(self):

		self.update_displays()
		self.master.mainloop()

	def update_displays(self):

		# Clear whatever is currently on the radar and aircraft summary screens
		self.radar_screen.delete(ALL)
		self.aircraft_summary_screen.delete(ALL)

		# Repaint the radar screen with the features selected via checkbuttons
		if self.radar_show_var_grid.get() == 1:
			self.paint_grid()
		
		if self.radar_show_var_crosshairs.get() == 1:
			self.paint_crosshairs()
		
		if self.radar_show_var_circles.get() == 1:
			self.paint_circles()
		
		if self.radar_show_var_degrees.get() == 1:
			self.paint_degrees()

		if self.radar_show_var_range.get() == 1:
			self.paint_range()

		# Update the list of aircraft being tracked if the conn_on button is selected
		# and mark the conn_status_indicator label accordingly
		if self.conn_status.get() == 1:
			url = 'http://' + self.ip_address + ':8080/data.json'
			self.tracker.get_flights(url)
			self.conn_status_indicator.config(text='GOOD', bg='green')

		# If the tracker encounters a connection error when get_flights() is called,
		# select the conn_off button so that the program is not stuck in a loop trying
		# to connect with the URL, then mark the conn_status_indicator label accordingly
		if self.tracker.connection_error == True:
			self.conn_off.select()
			self.conn_status_indicator.config(text='ERROR', bg='red')

		# If the conn_off button is selected but there wasn't a connection error
		# mark the conn_status_label as unknown
		if self.conn_status.get() == 0 and self.tracker.connection_error == False:
			self.conn_status_indicator.config(text='UNKN', bg='yellow')

		# Plot the currently tracked aircraft on the radar screen
		self.plot_aircraft()

		# List currently tracked aircraft on the aircraft summary screen
		self.print_summary()

		# Display the time when the tracker was last updated (position in top right corner)
		self.radar_screen.create_text(595, 2, anchor=NE, fill='green', font=('Courier', 8), text=self.tracker.current_time)

		# Display the IP address currently used (position in top right corner)
		self.radar_screen.create_text(595, 18, anchor=NE, fill='green', font=('Courier', 8), text='IP  ' + self.ip_address)

		# Display the unit of distance currently used (position in top left corner)
		self.radar_screen.create_text(5, 2, anchor=NW, fill='green', font=('Courier', 8), text='UNIT OF DIST: ' + self.unit_of_distance.upper())

		# Display the current lat and lon of the center position on the radar screen (position in bottom right)
		self.radar_screen.create_text(595, 582, anchor=SE, fill='green', font=('Courier', 8), text=('LAT  ' + str(self.current_lat).rjust(10)))
		self.radar_screen.create_text(595, 598, anchor=SE, fill='green', font=('Courier', 8), text=('LON  ' + str(self.current_lon).rjust(10)))

		# Repeate this process every 500 milliseconds
		self.master.after(500, self.update_displays)

	def paint_grid(self):

		# Horizontal lines
		self.radar_screen.create_line(0, 100, 600, 100, fill='green', dash=(4,4))
		self.radar_screen.create_line(0, 200, 600, 200, fill='green', dash=(4,4))
		self.radar_screen.create_line(0, 300, 600, 300, fill='green', dash=(4,4))
		self.radar_screen.create_line(0, 400, 600, 400, fill='green', dash=(4,4))
		self.radar_screen.create_line(0, 500, 600, 500, fill='green', dash=(4,4))

		# Vertical lines
		self.radar_screen.create_line(100, 0, 100, 600, fill='green', dash=(4,4))
		self.radar_screen.create_line(200, 0, 200, 600, fill='green', dash=(4,4))
		self.radar_screen.create_line(300, 0, 300, 600, fill='green', dash=(4,4))
		self.radar_screen.create_line(400, 0, 400, 600, fill='green', dash=(4,4))
		self.radar_screen.create_line(500, 0, 500, 600, fill='green', dash=(4,4))

	def paint_crosshairs(self):

		# Horizontal lines
		self.radar_screen.create_line(0, 300, 600, 300, fill='green', width=1)

		# Vertical lines
		self.radar_screen.create_line(300, 0, 300, 600, fill='green', width=1)

	def paint_degrees(self):

		self.radar_screen.create_text(305, 5, anchor=NW, fill='green', font=('Courier', 9), text='0 N')
		self.radar_screen.create_text(595, 280, anchor=NE, fill='green', font=('Courier', 9), text='90 E')
		self.radar_screen.create_text(305, 580, anchor=NW, fill='green', font=('Courier', 9), text='180 S')
		self.radar_screen.create_text(5, 280, anchor=NW, fill='green', font=('Courier', 9), text='270 W')

	def paint_range(self):

		# Divide the currently selected range by 3 to get the amound that each range label should be incremented
		increment = round((self.range.get() / 3), 0)
		increment = int(increment)

		# Display range labels at 3 places on each axis (example 20, 40, 60)
		self.radar_screen.create_text(295, 5, anchor=NE, fill='green', font=('Courier', 9), text=str(increment * 3))
		self.radar_screen.create_text(295, 105, anchor=NE, fill='green', font=('Courier', 9), text=str(increment * 2))
		self.radar_screen.create_text(295, 205, anchor=NE, fill='green', font=('Courier', 9), text=str(increment))

		self.radar_screen.create_text(5, 305, anchor=NW, fill='green', font=('Courier', 9), text=str(increment * 3))
		self.radar_screen.create_text(105, 305, anchor=NW, fill='green', font=('Courier', 9), text=str(increment * 2))
		self.radar_screen.create_text(205, 305, anchor=NW, fill='green', font=('Courier', 9), text=str(increment))

	def paint_circles(self):

		# Small circle
		self.radar_screen.create_oval(200, 200, 400, 400, outline='green', dash=(4,4))

		# Medium circle
		self.radar_screen.create_oval(100, 100, 500, 500, outline='green', dash=(4,4))

		# Large circle
		self.radar_screen.create_oval(0, 0, 600, 600, outline='green', dash=(4,4))

	def update_scale(self):

		self.lat_scale = calculations.get_scale(self.current_lat, self.current_lon, 'lat', self.range.get(), self.unit_of_distance)
		self.lon_scale = calculations.get_scale(self.current_lat, self.current_lon, 'lon', self.range.get(), self.unit_of_distance)

		# Divide by number of pixels from the center of the radar screen to the edge
		self.lat_scale = round((self.lat_scale / 300), 6)
		self.lon_scale = round((self.lon_scale / 300), 6)

	def update_unit_of_distance(self):
		if self.range_unit.get() == 1:
			self.unit_of_distance = 'km'

		elif self.range_unit.get() == 2:
			self.unit_of_distance = 'miles'

		self.update_scale()  # Scale needs to be updated to factor in the new unit of distance

	# Update the ip_address when user presses Enter key after typing into the conn_ip_entry field
	def update_ip_address(self, event):
		if len(self.conn_ip_entry.get()) > 0:
			self.ip_address = self.conn_ip_entry.get()
			self.master.focus()  # Reset focus after Enter is pressed (cursor is removed from entry field)

	# Update the current_lat and current_lon
	def update_latlon(self):

		# Get the values from the lat and lon entry fields, convert to floats, and update the current_lat/lon fields
		# If an error occurs (because value can't be converted to float), do nothing
		try:
			self.current_lat = float(self.lat_entry.get())
			self.current_lon = float(self.lon_entry.get())
			self.update_scale()  # Scale needs to be updated too with new lat and lon

		except ValueError:
			pass

	# Resets the lat and lon entry fields to display the default values from config file
	# then calls the update_latlon function
	def reset_latlon(self):
		self.lat_entry.delete(0, END)
		self.lon_entry.delete(0, END)
		self.lat_entry.insert(0, radar_config.DEFAULT_LAT)
		self.lon_entry.insert(0, radar_config.DEFAULT_LON)
		self.update_latlon()

	def plot_aircraft(self):

		tracking_list = []

		# Add values from the tracking entry fields to the tracking list if the lock button is selected
		if self.tracking1.get() == 1:
			tracking_list.append(self.tracking_entry1.get().upper())

		if self.tracking2.get() == 1:
			tracking_list.append(self.tracking_entry2.get().upper())

		if self.tracking3.get() == 1:
			tracking_list.append(self.tracking_entry3.get().upper())

		# Loop through each aircraft in the tracker object's aircraft list
		for aircraft in self.tracker.aircraft_list:

			if aircraft.validposition == 1:

				# Adding 300 adjusts for the fact that the center of canvas is actually at pixel coordinates (300,300)
				# whereas (0,0) is the top left corner of the canvas
				plot_lat = round(((self.current_lat - aircraft.lat) / self.lat_scale), 0) + 300
				plot_lon = round(((aircraft.lon - self.current_lon) / self.lon_scale), 0) + 300

				if plot_lat > 300:
					n = -1
				else:
					n = 1

				# If the aircraft is in the tracking list (locked on), do a few extra things besides just plot its position:
				# Calculate it's exact distance and bearing from the center point
				# Draw a line from the center point to the aircraft
				# Write its distance and bearing above its hex ID on the radar screen
				if aircraft.hex_code in tracking_list:
					self.radar_screen.create_line(plot_lon, plot_lat, 300, 300, fill='red')
					distance = calculations.get_distance(aircraft.lat, aircraft.lon, self.current_lat, self.current_lon, self.unit_of_distance)
					distance = str(int(round(distance)))
					bearing = calculations.get_bearing(self.current_lat, self.current_lon, aircraft.lat, aircraft.lon)
					bearing = str(int(round(bearing)))
					self.radar_screen.create_text((plot_lon - 5), (plot_lat - (33*n)), anchor=W, fill='red', font=('Courier', 8), text=('DIST ' + distance))
					self.radar_screen.create_text((plot_lon - 5), (plot_lat - (23*n)), anchor=W, fill='red', font=('Courier', 8), text=('BRG ' + bearing))
					self.radar_screen.create_image(plot_lon, plot_lat, anchor=CENTER, image=self.red_square)
					self.radar_screen.create_text((plot_lon - 5), (plot_lat - (13*n)), anchor=W, fill='red', font=('Courier', 8), text=aircraft.hex_code)

				else:
					self.radar_screen.create_image(plot_lon, plot_lat, anchor=CENTER, image=self.green_square)
					self.radar_screen.create_text((plot_lon - 5), (plot_lat - (13*n)), anchor=W, fill='green', font=('Courier', 8), text=aircraft.hex_code)
	
	# Helper function for print_summary(), returns true if aircraft meet all requirements to be printed
	def do_list(self, aircraft):

		# Assume aircraft meets requirements until marked False
		status = True
		if self.list_var_position.get() == 1 and aircraft.validposition == 0:
				status = False
				
		if self.list_var_flight.get() == 1 and aircraft.flight == 'N/A':
				status = False

		return status
		
	def print_summary(self):

		self.aircraft_summary_screen.create_text(5, 5, anchor=NW, fill='green', font=('Courier', 8), text=self.tracker.summary_headings())

		self.aircraft_summary_screen.create_line(0, 22, 700, 22, fill='green', width=1)

		y = 27
		for aircraft in self.tracker.aircraft_list:

			# Check to make sure the aircraft meets requirements to be listed if filter checkbuttons are selected
			if self.do_list(aircraft) == True:
				self.aircraft_summary_screen.create_text(5, y, anchor=NW, fill='green', font=('Courier', 8), text=aircraft.summary())
				y += 15