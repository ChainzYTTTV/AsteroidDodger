class Gravity:
    def __init__(self, gravity_strength=0.5, max_fall_speed=12, jump_force=-10):
        self.gravity_strength = gravity_strength
        self.max_fall_speed = max_fall_speed
        self.jump_force = jump_force

        self.velocity_y = 0.0
        self.on_ground = False

    def apply_gravity(self):
        if not self.on_ground:
            self.velocity_y += self.gravity_strength

            if self.velocity_y > self.max_fall_speed:
                self.velocity_y = self.max_fall_speed

    def jump(self):
        if self.on_ground:
            self.velocity_y = self.jump_force
            self.on_ground = False

    def land(self):
        self.velocity_y = 0.0
        self.on_ground = True

    def bonk_head(self):
        self.velocity_y = 0.0

    def leave_ground(self):
        self.on_ground = False