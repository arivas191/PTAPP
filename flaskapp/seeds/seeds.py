# from flask_seeder import Seeder

# class PTSeeder(Seeder):
#     # run() will be called by Flask-Seeder
#     def run(self):
#         # Create exercise objects
#         exercises = [
#             Exercise(
#                 title="Seated Knee Extension",
#                 description="This exercise is complete by sitting upright, bending your affected knee as far back as possible. Then holding and straightening your affected knee as far as possible and holding again, then relaxing. This motion helps strengthen your thigh muscles and aids in regaining range of motion in your knee.",
#                 body_part='Knee'
#             )
#         ]

#     # Create Exercises
#     for exercise in exercises:
#         print("Adding exercise: %s" % exercise)
#         self.db.session.add(exercise)


exercise = Exercise(
    title="Seated Knee Extension",
    description = "This exercise is complete by sitting upright, bending your affected knee as far back as possible. Then holding and straightening your affected knee as far as possible and holding again, then relaxing. This motion helps strengthen your thigh muscles and aids in regaining range of motion in your knee.",
    body_part="Knee"
)
db.session.add(exercise)
db.session.commit()
print("Adding exercise: %s" % exercise)
