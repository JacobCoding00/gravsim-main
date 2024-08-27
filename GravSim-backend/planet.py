class Planet:
    def __init__(self, mass, vel_x, vel_y, pos_x, pos_y):
        self.mass = mass
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.pos_x = pos_x
        self.pos_y = pos_y

    @property
    def get_mass(self):
        return self.mass

    @property
    def get_velocity_vector(self):
        return (self.vel_x, self.vel_y)

    @property
    def get_position_vector(self):
        return [self.pos_x, self.pos_y]

    def set_velocity(self, velocity):
        self.vel_x = velocity[0]
        self.vel_y = velocity[1]

    def set_position(self, position):
        print(position)
        self.pos_x = position[0]
        self.pos_y = position[1]

