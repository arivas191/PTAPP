import numpy as np

class ComputeMovementMetrics:
    # movements is a vector of input movements which is the raw data

    # metric 1 - the max max_distance the band was stretched
    max_distance

    # metric 2 - the max tension applied to the band
    max_tension

    # metric 3 - the number of repetitions in the workout
    repetitions

    # metric 4 - the duration of the workout
    duration

    __init__(self, movement):
        self.movements = movements

    find_max_distance():

    find_max_tension():

    find_repetitions():

    find_duration():
        start_time = self.movements[0].timestamp
        end_time = self.movements[-1].timestamp
        self.duration = end_time - start_time
