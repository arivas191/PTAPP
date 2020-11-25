from datetime import datetime, date
class ComputeMovementMetrics:
    """ movements is a vector of input movements which is the raw data
    metric 1 - the max distance the band was stretched
    metric 2 - the max force applied to the band
    metric 3 - the number of repetitions in the workout
    metric 4 - the duration of the workout
    assumptions: we record a minimum of 10 readings per second, all the force numbers are positive,
    for any repetition the max force is no less than 75% of the entire workout max strength
    """

    def __init__(self, movements):
        self.movements = movements
        self.max_distance = None
        self.max_force = None
        self.repetitions = None
        self.duration = None

    def find_max_distance(self):    # TODO figure some conversion from force to distance of the band using the spring const.
        self.max_distance = self.max_force*1 # need conversion

    def find_max_force(self):
        force_measurements = []
        for x in self.movements:
            force_measurements.append(x.force)
        self.max_force = max(force_measurements)

    def find_repetitions(self): # find the number of reps using force. this considers a positive change in force equal (with 20% margin) to at least 50% of the maximum force as a rep. 
       # reps = 0        # baseline means force has reached the lower threshold that marks the start of a new rep. 
        #self.force_measurements[1:] - self.force_measurments[0,end-1]
        #lower_threshold = self.max_force*.25
        #upper_threshold = self.max_force*.80 
        #baseline_met = True
        #for x in self.movements:
         #   if baseline_met: 
          #      if ((upper_threshold*.6) <= x.force <= (upper_threshold)):
           #         reps += 1
            #        baseline_met = False
           # else:
            #    if ((lower_threshold*.9) <= x.force <= (lower_threshold*1.1)):
             #       baseline_met = True
       
        reps = 0
        count = 0
        for i in range(1, len(self.movements) - 1):
            if self.movements[i].force > self.movements[i - 1].force and self.movements[i].force > 2:
                count += 1
            elif self.movements[i].force < self.movements[i - 1].force and count >= 4:
                reps += 1
                count = 0
        self.repetitions = reps


        

    def find_duration(self):
        start_time = self.movements[0].timestamp
        end_time = self.movements[-1].timestamp
        self.duration = datetime.combine(date.today(), end_time) - datetime.combine(date.today(), start_time)
