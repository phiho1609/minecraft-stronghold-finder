import math
import numpy
import time


def main():
    DEBUG_TAG = "main: "

    input_1, input_2 = shell_welcome()

    print(DEBUG_TAG, "input 1: ", input_1.x, input_1.z, input_1.angle)
    print(DEBUG_TAG, "input 2: ", input_2.x, input_2.z, input_2.angle)

    result = calc(input_1, input_2)
    if result.angle == -1:
        print("failed.")

    print("\n##############################################")
    print("\nThe Stronghold is at: ", int(result.x), int(result.z))
    time.sleep(1)
    print("\n\nPress Enter to close the Program...")
    input()


def shell_welcome():
    print("\n")
    print("Minecraft Stronghold Calaculator.")
    print("by DrTierlieb")
    print("\n")
    time.sleep(1)
    print("You will need to input a coordinates (x,z)\nand the respectively given angle from two thrown endereyes.")
    time.sleep(0.2)
    print("Please follow the upcoming instructions.")
    time.sleep(0.2)

    x1 = 0
    z1 = 0
    angle1 = 0
    x2 = 0
    z2 = 0
    angle2 = 0

    def list_string2float_tuple(list_string):
        float_tuple_str = list_string.split(',')
        if len(float_tuple_str) != 2:
            raise RuntimeError('Two comma-separated coordinates were expected, ' + str(len(float_tuple_str)) + " were given!" )

        return (float(float_tuple_str[0]), float(float_tuple_str[1]))


    print("\n##############################################")
    print("Go to the first point and enter the X- and Z-Coordinate, separated by a comma.")
    time.sleep(0.2)
    print("Coordinates of Point 1: ")
    x1, z1 = list_string2float_tuple(input())
    time.sleep(0.5)
    print("Now don't move, throw an ender-eye and focus its final floating position with your crosshair.")
    print("Do not move your crosshair after you have it on the final position!")
    print("Now, with your crosshair in position, press F3. On the left side, in the second paragraph there should be a line starting with 'Facing: <north/east/south/west>...'.")
    print("At the end of that line there are two values in parantheses. The FIRST value is the horizontal angle, the value of interest, enter that now.")
    print("Horizontal Angle: ")
    angle1 = float(input())
    time.sleep(0.5)

    print("\n##############################################")
    print("Now repeat for a second point. The further away from the first, the more precise the calculation, but 50-100 blocks seem to be enough.")
    print("Hint: Try to choose the second point perpendicular to the trajectory direction of the first ender-eye throw.")
    print("Now, again, enter X- and Z-Coordinate of your second point.")
    time.sleep(0.2)
    print("Coordinates of Point 2:")
    x2, z2 = list_string2float_tuple(input())
    time.sleep(0.5)
    print("Throw the eye, focus with your crosshair, and read the horizontal angle.")
    print("Horizontal Angle: ")
    angle2 = float(input())
    time.sleep(0.5)

    print("Now follows: Crap ton of bullshit")

    return (Data(x1, z1, angle1), Data(x2, z2, angle2))


def calc(p1, p2):
    DEBUG_TAG = "calc: "
    # Fixing Angles to 0 - 360
    if p1.angle < 0:
        p1.angle += 360
    if p2.angle < 0:
        p2.angle += 360

    print(DEBUG_TAG, "angles after 0 - 360 conversion: \np1: ", p1.angle, "\np2: ", p2.angle)

    normalised_list = get_normalised_points(p1, p2)

    n_p1, n_p2 = normalised_list[0]
    rot_origin = normalised_list[1]
    rot_angle = normalised_list[2]

    print(DEBUG_TAG, "point angles after normalising: \np1: ", n_p1.angle, "\np2: ", n_p2.angle)

    # if angles should point "down" -> mirror upwards
    flip = False
    if n_p1.angle > 90 and n_p1.angle < 270:         # angles ar normalised => p1 is left  => p1.angle points down right
        if n_p2.angle > 90 and n_p2.angle < 270:     #                         p2 is right => p2.angle points down left
            flip = True
            print(DEBUG_TAG, "Flip is required (angles point downwards)")
        else:
            print("calc: angles got fucked up through transformation")
            return Data(0, 0, -1)

    """check if lines will ever meet => otherwise no solution"""

    if (not flip and p1.angle >= p2.angle) or (flip and p1.angle <= p2.angle):
        print("No possible solution. \nMaybe the coordinates were to close to each other?")
        return Data(0, 0, -1)


    alpha = abs(270 - n_p1.angle) if abs(270 - n_p1.angle) <= 180 else 360 - abs(270 - n_p1.angle)
    beta = abs(90 - n_p2.angle) if abs(90 - n_p2.angle) <= 180 else 360 - abs(90 - n_p2.angle)
    gamma = (180 - alpha - beta) % 360

    print(DEBUG_TAG, "alpha: ", alpha, "beta: ", beta, "gamma: ", gamma)

    c_side = abs(n_p1.x - n_p2.x) # length of c side (p1 to p2)
    b_side = c_side * (math.sin(math.radians(beta)) / math.sin(math.radians(gamma))) # length of b side (p1 to goal)

    print(DEBUG_TAG, "p1 to p2: ", c_side, ", p1 to goal: ", b_side)

    rel_goal_x = b_side * math.cos(math.radians(alpha))
    rel_goal_z = b_side * math.sin(math.radians(alpha))
    print(DEBUG_TAG, "relative coords: ", rel_goal_x, ", ", rel_goal_z)

    """undo transformation"""
    abs_goal_x = rel_goal_x + n_p1.x
    abs_goal_z = rel_goal_z + n_p1.z
    print(DEBUG_TAG, "absolute coords: ", abs_goal_x, ", ", abs_goal_z)

    if flip:
        abs_goal_z = n_p1.z - rel_goal_z    # x didnt change through vertical mirroring => only mirror z
        print(DEBUG_TAG, "Flip was required, after flip: ", abs_goal_x, ", ", abs_goal_z)

    print(DEBUG_TAG, "rot_origin: ", rot_origin, ", abs_goal: ", (abs_goal_x, abs_goal_z), ", rot_angle: ", rot_angle)
    final_coords = rotate(rot_origin, (abs_goal_x, abs_goal_z), math.radians(-rot_angle))

    print(DEBUG_TAG, "After Final back rotation: ", final_coords[0], ", ", final_coords[1])

    return Data(final_coords[0], final_coords[1], 0)



def get_plumb_line(p1, p2):
    diff_x = p1.x - p2.x
    diff_z = p1.z - p2.z
    line_angle = math.degrees(math.atan2(diff_x, diff_z))
    line_angle = line_angle + 360 if line_angle < 0 else line_angle

    return (line_angle + 90) % 360

def get_normalised_points(p1, p2):
    """rotates p1 and p2 around the middle, so z is the same (horizontal line)"""
    DEBUG_TAG = "get_normalised_points: "
    diff_x = p2.x - p1.x
    diff_z = p2.z - p1.z
    line_angle = (math.degrees(math.atan2(diff_z, diff_x)) - 90) % 360
    line_angle = line_angle + 360 if line_angle < 0 else line_angle
    print(DEBUG_TAG, "line_angle: ", line_angle)
    # angle of [p1,p2] in degrees is ready

    origin_x = p1.x + (abs(diff_x)/2) if p1.x < p2.x else p2.x + (abs(diff_x)/2)
    origin_z = p1.z + (abs(diff_z)/2) if p1.z < p2.z else p2.z + (abs(diff_z)/2)
    origin = (origin_x, origin_z)
    point_p1 = (p1.x, p1.z)
    point_p2 = (p2.x, p2.z)
    rotation_angle = 270 - line_angle       # 270° equals an horizontal line, pos rotation_angle = counterclockwise rot, neg rotation_angle = clockwise rot
    print(DEBUG_TAG, "origin of rotation: ", origin)
    print(DEBUG_TAG, "rotation_angle: ", rotation_angle)
    print("#rotation_angle: ", rotation_angle)
    normal_p1 = rotate(origin, point_p1, math.radians(rotation_angle))
    print("#rotation_angle: ", rotation_angle)
    normal_p2 = rotate(origin, point_p2, math.radians(rotation_angle))
    print("#rotation_angle: ", rotation_angle)

    new_p1 = Data(normal_p1[0], normal_p1[1], 0)
    new_p2 = Data(normal_p2[0], normal_p2[1], 0)

    print(DEBUG_TAG, "Normalised coords: ", new_p1.x, ", ", new_p1.z, " and ", new_p2.x, ", ", new_p2.z)

    """normalize angles of p1 and p2"""
    new_p1.angle = (p1.angle + rotation_angle) % 360
    new_p2.angle = (p2.angle + rotation_angle) % 360
    print("#rotation_angle: ", rotation_angle)

    return [(new_p1, new_p2), origin, rotation_angle]


def rotate(origin, point, angle):
    """
    Rotate a point counterclockwise by a given angle(in radians) around a given origin.
    x increases from left to right
    y increases from down to up
    The angle should be given in radians.
    """
    DEBUG_TAG = "rotate: "
    print(DEBUG_TAG, "called with origin: ", origin, ", angle: ", math.degrees(angle), "for point: ", point)

    ox, oy = origin
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy

class Data():
    def __init__(self, x, z, angle):
        self.x      = x
        self.z      = z
        self.angle  = angle




def debug_atan2():
    points = [[0, 100],[100, 100],[100, 0],[100, -100],[0, -100],[-100, -100], [-100, 0], [-100, 100]]

    for i in range(0, len(points)):
        tmp = (math.degrees(math.atan2(points[i][1], points[i][0])) - 90) % 360
        tmp = tmp + 360 if tmp < 0 else tmp
        print(tmp)

    """base = (1,0,0)
    
    for i in range (0, )
    target = dest[0], dest[1]
    p_axis = -base[1], base[0]
    b_axis = base[0], base[1]

    x_proj = numpy.dot(target, b_axis)
    y_proj = numpy.dot(target, p_axis)

    result = math.degrees(math.atan2(y_proj, x_proj))

    return (result + 360) % 360"""


def debug_transform():
    p1 = Data(200, -100, 0)
    p2 = Data(-200, 100, 0)

    print("Point 1: ", p1.x, p1.z)
    print("Point 2: ", p2.x, p2.z)

    list = get_normalised_points(p1, p2)
    new_p1, new_p2 = list[0]
    origin = list[1]
    rot = list[2]
    print("after transformation around origin: ", origin, "with an angle of: ", rot)
    print("Point 1: ", new_p1.x, new_p1.z)
    print("Point 2: ", new_p2.x, new_p2.z)



if __name__ == "__main__":
    main()
    #debug_atan2()
    #debug_transform()