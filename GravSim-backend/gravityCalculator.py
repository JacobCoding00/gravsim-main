import math
import time

from planet import Planet

G = 1

def calculate_gravity(planet_array, time):
    for i in planet_array:
        if not i.is_eliminated():
            total_acc_x = 0
            total_acc_y = 0
            for j in planet_array:
                if j != i:
                    # calculate distance between two planets
                    distance_x = i.pos_x - j.pos_x
                    distance_y = i.pos_y - j.pos_y
                    distance_squared = distance_x * distance_x + distance_y * distance_y
                    # calculate acceleration using GMM/r^2
                    acceleration = (G * j.get_mass) / distance_squared

                    # calculate angle of line drawn between the two planets
                    angle = math.atan2(distance_y , distance_x)
                    # use it to calculate the acceleration in each vector
                    acc_x = math.cos(angle) * acceleration
                    acc_y = math.sin(angle) * acceleration
                    # add to total
                    total_acc_x -= acc_x
                    total_acc_y -= acc_y

            # calculate new velocity vector for each planet
            new_vel_x = i.get_velocity_vector[0] + total_acc_x * time
            new_vel_y = i.get_velocity_vector[1] + total_acc_y * time
            # enforce a speed limit on planets to avoid them shooting off in close encounters
            if new_vel_x >= 3:
                new_vel_x = 3
            if new_vel_y >= 3:
                new_vel_y = 3
            if new_vel_x <= -3:
                new_vel_x = -3
            if new_vel_y <= -3:
                new_vel_y = -3
            i.set_velocity([new_vel_x, new_vel_y])

            # calculate new position of each planet
            new_pos_x = i.get_position_vector[0] + i.get_velocity_vector[0] * time
            new_pos_y = i.get_position_vector[1] + i.get_velocity_vector[1] * time
            if new_pos_x > 1000 or new_pos_x < 0 or new_pos_y < 0 or new_pos_y > 1000:
                i.eliminate()
            i.set_position([new_pos_x, new_pos_y])


