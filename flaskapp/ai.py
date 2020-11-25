import numpy as np 
from sklearn.model_selection import train_test_split
from sklearn import svm
""" The training set is user movements that have a manual calculation of the category.
 Discrete categories include beginner, intermediate, and advanced.
 A dataset is a dictionary-like object with n_samples and n_features. Dataset is formatted in a 2D array. """
class AI:

    def __init__(self, strength, reps, exercise_body_part):  # Valid inputs for exercise are 'Arm', 'Ankle', 'Shoulder', 'Hips', and 'Knee'
        self.strength = np.array([[strength]])
        self.reps = np.array([[reps]])
        self.exercise = exercise_body_part

    def run(self):
        movement_training = self.get_training_data()
        x = movement_training[:,:-1] 
        y = movement_training[:,-1] 

        ai = svm.SVC(gamma=0.001) # gamma taken from the digits example
        ai.fit(x, y) # fit the classifier to the data (calibrate)
        strength_feedback = ai.predict(self.strength) # get the category
        if strength_feedback[0] == 1.0:
            return 'Beginner'
        if strength_feedback[0] == 2.0:
            return 'Intermediate'
        if strength_feedback[0] == 3.0:
            return 'Advanced'
        #return strength_feedback

    def get_training_data(self):
        global beginner
        global intermediate
        global advanced
        beginner = 1
        intermediate = 2
        advanced = 3

        curl_ideal_force = 10.4
        hip_ideal_force = 8.7
        knee_ideal_force = 8.2

        if self.exercise == 'Arm':
            return self.construct_array(curl_ideal_force)
        elif self.exercise == 'Hips':
            return self.construct_array(hip_ideal_force)
        elif self.exercise == 'Knee':
            return self.construct_array(knee_ideal_force)
        # elif self.exercise == 'Ankle':
        #     return np.array([])
        # elif self.exercise == 'Shoulder':
        #     return np.array([])

    def construct_array(self, ideal_force):
        return np.array([
                    [ideal_force,advanced],
                    [ideal_force*0.92,advanced],
                    [ideal_force*0.85,advanced],
                    [ideal_force*0.84,intermediate],
                    [ideal_force*0.70,intermediate],
                    [ideal_force*0.61,intermediate],
                    [ideal_force*0.59,beginner],
                    [ideal_force*0.40,beginner],
                    [ideal_force*0.30,beginner]
                ])

    #Hardcoded values for the workouts, these should probably live as constant variables in the scikit method
    # curl_ideal_force = 10.4
    # curl_ideal_repetitions = 8
    # curl_weak_force = 6.3
    # curl_weak_repetitions = 5

    # hip_abd_ideal_force = 8.7
    # hip_abd_ideal_repetitions = 6
    # hip_abd_weak_force = 5.2
    # hip_abd_weak_repetitions = 3

    # knee_ext_ideal_force = 8.2
    # knee_ext_ideal_repetitions = 4
    # knee_ext_weak_force = 5.3
    # knee_ext_ideal_repetitions = 4
