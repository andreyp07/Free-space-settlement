import math

def calculate_major_radius(w_rad):
    g = 9.807

    major_radius = g / (w_rad ** 2)

    return major_radius


def check_condition_4(major_radius, h):
    return major_radius >= (10 * h)


def calculate_b(major_radius, useful_area):
    b = useful_area / (2 * math.pi * major_radius)

    return b


def calculate_a1(b, h, major_radius, c):

    k = (1 - ((b - c) ** 2)/(b ** 2)) ** 1/2

    a_1 = (major_radius - 10 * h) / (10 * (k + 1))

    return a_1


def calculate_a2(a_1, b, c, l, h):

    k = math.sqrt(1 - ((b - c) ** 2) / (b ** 2))

    a_2 = a_1 + (l + h) / k

    return a_2


def check_condition_8(a_1, b, beta):

    variable = math.atan(a_1 / b)

    conversion_to_degrees = variable * (360 / (2 * math.pi))

    return conversion_to_degrees >= beta


def check_condition_9(a_1, b, theta):

    variable = math.atan(a_1 / b)

    conversion_to_degrees = variable * (360 / (2 * math.pi))

    return conversion_to_degrees <= theta


def check_condition_11_v2(useful_area, a_1, b, major_radius):

    return calculate_actual_useful_area(a_1, b, major_radius) >= useful_area


def check_condition_11_v3(useful_area, epsilon, a_1, b, major_radius):
    return abs(calculate_actual_useful_area(a_1, b, major_radius) - useful_area) <= epsilon


def check_condition_12_v2(a_1, a_2, b, major_radius, useful_volume):

    real_volume = calculate_useful_real_volume(a_1, a_2, b, major_radius)

    return real_volume >= useful_volume


def calculate_useful_real_volume(a_1, a_2, b, major_radius):

    if (major_radius - 10 * a_1) > (10 * a_2):

        useful_real_volume = calculate_total_volume(a_1, a_2, b, major_radius)

        return useful_real_volume

    else:

        variable_1 = 2 * math.acos((major_radius - 10 * a_1) / (10 * a_2))

        useful_real_volume = major_radius * b * \
                             math.pi * (a_1 * math.pi + a_2 * math.pi -
                                        a_2 * (variable_1 - math.sin(variable_1)))

        return useful_real_volume


def calculate_total_volume(a_1, a_2, b, major_radius):

    volume = major_radius * b * (math.pi**2) * (a_1 + a_2)

    return volume


def calculate_total_area(a_1, a_2, b, major_radius):

    perimeter_1 = perimeter(a_1, b)

    perimeter_2 = perimeter(a_2, b)

    area = math.pi * major_radius * (perimeter_1 + perimeter_2)

    return area


def perimeter(a, b):
    H = ((a - b) / (a + b)) ** 2

    perimeter = math.pi * (a + b) * (1 + ((3 * H) / (10 + math.sqrt(4 - 3 * H))) +

                                     ((4 / math.pi) - (14 / 11)) * (H ** 12))

    return perimeter


def calculate_actual_useful_area(a_1, b, major_radius):

    actual_area = math.pi * major_radius * perimeter(a_1, b)

    return actual_area


def calculate_structure(number_persons, area_person, volume_person,
                        height_building, w_initial, c, l, i, u, theta, beta, epsilon):
    """

    :param number_people: number of people of the settlement
    :param area_person: area per person required
    :param volume_person: volume per person required
    :param height_building: height of tallest building
    :param w_initial: initial angular velocity (in rpms)
    :param c: distance between last building and structure wall
    :param l: minimum distance above each building
    :param i: quantity by which we increase the angular velocities
    :param u: quantity by which a_1 and b are multiplied if their area is far from epsilon
    :param theta: maximum angle for tan^-1(a_1/b)
    :param beta: minimum angle for tan^-1(a_1/b)
    :param epsilon: quantity that the useful real area may exceed the useful ideal area
    :return: the list of the possible structures

    """

    structures = []

    useful_area = number_persons * area_person

    useful_volume = number_persons * volume_person

    w = w_initial

    while w < 6:

        w += i

        print(w)

        w_rad = w * ((2 * math.pi) / 60)

        major_radius = calculate_major_radius(w_rad)

        if check_condition_4(major_radius, height_building):

            b = calculate_b(major_radius, useful_area)

            a_1 = calculate_a1(b, height_building, major_radius, c)

            condition_8 = True

            while not (check_condition_8(a_1, b, beta)):

                b -= 0.01  # antes: b -= 0.25

                a_1 = calculate_a1(b, height_building, major_radius, c)

                condition_8 = False

            else:

                condition_9 = True

                while not (check_condition_9(a_1, b, theta)):

                    condition_9 = False

                    if not condition_8:

                        continue

                    else:

                        a_1 -= 0.5

                if not check_condition_8(a_1, b, beta):

                    continue

                else:

                    while not check_condition_11_v2(useful_area, a_1, b, major_radius):

                        if condition_8 and condition_9:

                            print("Type 2 contradiction", w)

                            continue

                        else:

                            a_1 *= 1.5

                            b *= 1.5

                    while not check_condition_11_v3(useful_area, epsilon, a_1, b, major_radius):

                        b *= u

                        a_1 *= u

                        if not check_condition_11_v2(useful_area, a_1, b, major_radius):

                            a_1 = a_1 / u

                            b = b / u

                            u += u / 1000  # we can decrease to u / 10000

                    a_2 = calculate_a2(a_1, b, c, l, height_building)

                    """if not check_condition_12_v2(a_1, a_2, b, major_radius, useful_volume):
                        print("Type 3 contradiction", w)

                        continue"""

                    useful_real_volume = calculate_useful_real_volume(a_1, a_2, b, major_radius)

                    useful_real_area = calculate_actual_useful_area(a_1, b, major_radius)

                    total_volume = calculate_total_volume(a_1, a_2, b, major_radius)

                    total_area = calculate_total_area(a_1, a_2, b, major_radius)

                    structures.append([a_1, a_2, b, major_radius, math.atan(a_1/b),
                                       useful_real_volume, useful_real_area, total_volume,
                                       total_area])

        else:

            print("Type 1 contradiction", w)

            return structures

    return structures


if __name__ == '__main__':

    print(calculate_structure(10000, 67, 823, 9, 0.75, 7, 4, 0.05, 0.95, 30, 10, 500))
