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
        strength_movement_training, endurance_movement_training = self.get_training_data()
        strength_x = strength_movement_training[:,:-1] 
        strength_y = strength_movement_training[:,-1] 
        endurance_x = endurance_movement_training[:,:-1]
        endurance_y = endurance_movement_training[:,-1]

        ai_strength = svm.SVC(gamma=0.001) # gamma taken from the digits example
        ai_strength.fit(strength_x, strength_y) # fit the classifier to the data (calibrate)
        strength_feedback = ai_strength.predict(self.strength) 

        ai_endurance = svm.SVC(gamma=0.001)
        ai_endurance.fit(endurance_x, endurance_y)
        endurance_feedback = ai_endurance.predict(self.reps)

        return self.convert_level_to_string(strength_feedback), self.convert_level_to_string(endurance_feedback)

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
        # ankle_ideal_force
        # shoulder_ideal_force

        curl_ideal_reps = 8
        hip_ideal_reps = 6
        knee_ideal_reps = 7
        # ankle_ideal_reps
        # shoulder_ideal_reps

        if self.exercise == 'Arm':
            strength = self.construct_array(curl_ideal_force)
            endurance = self.construct_array(curl_ideal_reps)
        elif self.exercise == 'Hips':
            strength = self.construct_array(hip_ideal_force)
            endurance = self.construct_array(hip_ideal_reps)
        elif self.exercise == 'Knee':
            strength = self.construct_array(knee_ideal_force) 
            endurance = self.construct_array(knee_ideal_reps)
        # elif self.exercise == 'Ankle':
        #     strength = self.construct_array(ankle_ideal_force) 
        #     endurance = self.construct_array(ankle_ideal_reps)
        # elif self.exercise == 'Shoulder':
        #     strength = self.construct_array(shoulder_ideal_force) 
        #     endurance = self.construct_array(shoulder_ideal_reps)

        return strength, endurance

    def construct_array(self, ideal):
        return np.array([
                    [ideal,advanced],
                    [ideal*0.92,advanced],
                    [ideal*0.85,advanced],
                    [ideal*0.84,intermediate],
                    [ideal*0.70,intermediate],
                    [ideal*0.61,intermediate],
                    [ideal*0.59,beginner],
                    [ideal*0.40,beginner],
                    [ideal*0.30,beginner]
                ])
    def convert_level_to_string(self, level):
        if level == 1:
            return 'Beginner'
        elif level == 2:
            return 'Intermediate'
        elif level == 3:
            return 'Advanced'