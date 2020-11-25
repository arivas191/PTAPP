from flaskapp import app, db
from flaskapp.ai import AI
import click
import numpy as np 

""" the category manual calculation is based on the following bounds for both strength and reps:
    beginner: (0 to 60%)  of ideal 
    intermediate: [60% to 85%) of ideal 
    advanced: [85% to 150%) of ideal  """

@click.command()
def test_ai():
    movements_tester = np.array([  # formatted exercise, strength, strength category manual calculation, reps, endurance category manual calculation
            ['Arm', 8.2, 'Intermediate', 7, 'Advanced'],
            ['Arm', 4.9, 'Beginner', 1, 'Beginner'],
            ['Hips', 3.5, 'Beginner', 4, 'Intermediate'],
            ['Hips', 6.1, 'Intermediate', 9, 'Advanced'],
            ['Knee', 9.3, 'Advanced', 2, 'Beginner'],
            ['Knee', 2.5, 'Beginner', 12, 'Advanced']
        ])
    for movement in movements_tester:
        exercise = movement[0]
        strength = movement[1]
        reps = movement[3]
        manual_category_strength = movement[2]
        manual_category_enduracne = movement[4]
        click.echo("strength: %s" % strength)
        click.echo("reps: %s" % reps)
        click.echo("manual strength category calculation: %s" % manual_category_strength)
        click.echo("manual endurance category calculation: %s" % manual_category_enduracne)

        ai = AI(strength, reps, exercise)
        strength_feedback, endurance_feedback = ai.run()
        click.echo("ai strength category calculation: %s" % strength_feedback)
        click.echo("ai endurance category calculation: %s" % endurance_feedback)

if __name__ == '__main__':
    test_ai()
