# the pseudocode to instantiate this
# movements_list = list[]

# for connection to excel file open:
    # while the a next row is not null
        # list.append(InputMovement(currentdata))

class InputMovement:

    def __init__(self, timestamp, force, x, y, z):
        self.timestamp = timestamp
        self.force = force
        self.acceleration_x = x
        self.acceleration_y = y
        self.acceleration_z = z
