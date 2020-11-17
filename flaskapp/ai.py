import numpy as np 
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn import svm
""" The training set is user movements that have a manual calculation of the category.
 Discrete categories include beginner, intermediate, and advanced.
 A dataset is a dictionary-like object with n_samples and n_features. Dataset is formatted in a 2D array. """
class AI:

    def __init__(self, movement_metrics, exercise):  # Valid inputs for exercise are 'Arm', 'Ankle', 'Shoulder', 'Hips', and 'Knee'
        self.movement_metrics = movement_metrics
        self.exercise = exercise

    def run(self):
        if self.exercise == 'Arm':
            movement_training = np.array([[1,3,2],[1,2,0],[1,4,3]]) # strength, endurance, category
        elif self.exercise == 'Ankle':
            movement_training = np.array([[],[],[]])
        elif self.exercise == 'Shoulder':
            movement_training = np.array([[],[],[]])
        elif self.exercise == 'Hips':
            movement_training = np.array([[],[],[]])
        elif self.exercise == 'Knee':
            movement_training = np.array([[],[],[]])

        x = movement_training[:-1,:] 
        y = movement_training[-1,:] 
        C = 10 # taken from an example - penalty param of the error term

        # instantiate the classifier
        ai = svm.SVC(C=C, random_state=0)
        # fit the classifier to the data (calibrate)
        ai.fit(x, y)
        return ai.predict(movement_metrics) # get the category