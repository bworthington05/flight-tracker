import os
import sys

sys.path.append(os.path.join(os.getcwd(), 'lib'))

from radar_gui import *

app = GUI()
app.run()