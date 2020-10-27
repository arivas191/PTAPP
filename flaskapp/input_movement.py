# the pseudocode to instantiate this 
# movements_list = list[]

# for connection to excel file open:
    # while the a next row is not null
        # list.append(InputMovement(currentdata))

import numpy as np

class InputMovement:
    # movements is a vector of input movements which is the raw data
    # where x = , y = , and z = 

    name_for_x

    name_for_y

    name_for_z    
    
    # the time of the data measurement in utc datetime
    timestamp

    __init__(self, x, y, z, timestamp):
        self.name_for_x = x
        self.name_for_y = y
        self.name_for_z = z
        self.timestamp = timestamp