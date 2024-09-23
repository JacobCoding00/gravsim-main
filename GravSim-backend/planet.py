import math


class Planet:
    def __init__(self, mass, vel_x, vel_y, pos_x, pos_y,):
        self.mass = mass
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.eliminated = False
        self.merged_to = []

    @property
    def get_mass(self):
        return self.mass

    @property
    def get_velocity_vector(self):
        return [self.vel_x, self.vel_y]

    @property
    def get_position_vector(self):
        return [self.pos_x, self.pos_y]
   
    def set_velocity(self, velocity):
        self.vel_x = velocity[0]
        self.vel_y = velocity[1]

    def set_position(self, position):
        self.pos_x = position[0]
        self.pos_y = position[1]

    def eliminate(self):
        self.eliminated = True

    def is_eliminated(self):
        return self.eliminated

    @property
    def get_angle_and_speed(self):
        speed = math.sqrt((self.vel_x * self.vel_x) + (self.vel_y * self.vel_y))
        angle = math.atan2(self.vel_y , self.vel_x)
        return [angle, speed]

    def merge_with(self, planet):
        self.merged_to.append(planet)

    def get_merge(self):
        return self.merged_to

