class ComputeMovementMetrics:
    """ movements is a vector of input movements which is the raw data
    metric 1 - the max distance the band was stretched
    metric 2 - the max force applied to the band
    metric 3 - the number of repetitions in the workout
    metric 4 - the duration of the workout
    assumptions: we record a minimum of 10 readings per second, all the force numbers are positive,
    for any repetition the max force is no less than 75% of the entire workout max strength
    """

    __init__(self, movements):
        self.movements = movements

    find_max_distance():    # TODO figure some conversion from force to distance of the band using the spring const.
        self.max_distance = self.max_force*some_conversion

    find_max_force():
        force_measurements = []
        for x in self.movements:
            force_measurements.append(x.force)
        self.max_force = max(force_measurements)

    find_repetitions(): # find the number of reps using force. this considers a positive change in force equal (with 20% margin) to at least 50% of the maximum force as a rep. 
        reps = 0        # baseline means force has reached the lower threshold that marks the start of a new rep. 
        lower_threshold = self.max_force*.75
        upper_threshold = self.max_force*.25 
        baseline_met = True
        for x in self.movements:
            if baseline_met: 
                if ((upper_threshold*.9) <= x.force <= (upper_threshold*1.1)):
                    reps += 1
                    baseline_met = False
            else:
                if ((lower_threshold*.9) <= x.force <= (lower_threshold*1.1)):
                    baseline_met = True
        self.repetitions = reps 

    find_duration():
        start_time = self.movements[0].timestamp
        end_time = self.movements[-1].timestamp
        self.duration = end_time - start_time
