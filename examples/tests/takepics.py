import cozmo
import asyncio
import time

from cozmo.util import Angle


def take_pics(robot: cozmo.robot.Robot):
    robot.move_lift(-3.0)
    robot.set_head_angle(cozmo.robot.MAX_HEAD_ANGLE).wait_for_completed()

    face: cozmo.faces.Face = None

    while True:

        if face and face.is_visible:

            print("Found a face.")
            robot.camera.color_image_enabled = True
            robot.world.latest_image.raw_image.show()
            print(face.name)
            return

        else:

            try:
                print("Searching a face.")
                face = robot.world.wait_for_observed_face(timeout=10)
            except asyncio.TimeoutError:
                print("Didn't find a face.")
                robot.turn_in_place(Angle(degrees=60.0)).wait_for_completed()

        time.sleep(.1)


cozmo.run_program(take_pics, use_viewer=True, force_viewer_on_top=False)
