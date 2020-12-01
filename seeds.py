from flaskapp import app, db
from flaskapp.models import *
import click

@click.command()
def seeds():
    """Saves all the exercises in the database."""
    exercises = [
        Exercise(
            id=1,
            title="Seated Knee Extension",
            description='This exercise is complete by sitting upright, bending your affected knee as far back as possible. Then holding and straightening your affected knee as far as possible and holding again, then relaxing. This motion helps strengthen your thigh muscles and aids in regaining range of motion in your knee.',
            body_part="Knee",
            image_name="SeatedKneeExtension.png",
            demo_link="https://www.youtube.com/embed/1nSE-RMtYJo"
        ),
        Exercise(
            id=2,
            title="Bicep Curl",
            description='This exercise is completed by placing the resistance band under your feet and slowly curl your hand up to the shoulder, squeezing the bicep and keeping your elbow next to your side. Then slowly release your arm back down to starting postition and repeat with both arms.',
            body_part="Arm",
            image_name="bicep.jpeg",
            demo_link="https://www.youtube.com/embed/cjtdsi9BzxA"
        ),
        Exercise(
            id=3,
            title="Shoulder External Rotation",
            description='This exercise is completed by keeping the elbow fixed and externally rotating at the shoulder to raise the band up towards the ceiling as without lifting the elbow. It strengthens your infraspinatus muscle to Improve overhead lifting and reaching',
            body_part="Shoulder",
            image_name="ShoulderExternalRotation.png",
            demo_link="https://www.youtube.com/embed/cFyP6e4XeGo"
        ),
        Exercise(
            id=4,
            title="Side Hip Abduction",
            description='This exercise is completed by laying down on the floor on your side with your head on your arm and legs bent at the knee. Keeping your feet together, lift the top leg up so that your knees are separated and then lower your leg back down slowly. This motion strengthens the hip muscles and relieves patellofemoral pain syndrome -- aka "Runner’s Knee”.',
            body_part="Hips",
            image_name="SideHipAbduction.png",
            demo_link="https://www.youtube.com/embed/_3v512ODfQM"
        ),
        Exercise(
            id=5,
            title="Way Ankle Exercises",
            description='“A) Dorsiflexion: The pull or resistance should be pulling the foot down, so that you have to pull your foot/toes up towards you. (You may need someone to hold the band for you) -You can also anchor the other end of the tubing by tying a knot in the tubing, placing it between a door and frame then closing the door.  B) Plantarflexion: Hold band in hand so that the resistance is pulling the foot up towards you. Push foot down as if to push a gas pedal.  C) Inversion: Cross legs so the "injured” foot is under the "uninjured” leg, loop the band around the "uninjured” foot, holding the end of the band tight in hands. The resistance should want to pull the "injured” foot towards the other foot. Push the foot/ankle away from the other foot. D) Eversion: With both legs straight out about shoulder width apart, wrap the band around the ball of the "injured” foot then loop the other foot and hold the band. The resistance should pull the foot in towards the other foot. You will want to push the "injured” foot out away from the other foot”',
            body_part="Ankle",
            image_name="WayAnkleExercises.png",
            demo_link="https://www.youtube.com/embed/AyxqS1g1vdU"
        )
    ]

    for exercise in exercises:
        click.echo("Adding exercise: %s" % exercise)
        db.session.add(exercise)
        db.session.commit()

if __name__ == '__main__':
    seeds()
