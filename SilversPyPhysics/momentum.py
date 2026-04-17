class Momentum:
    def __init__(self, acceleration=0.5, friction=0.35, max_speed=5):
        self.acceleration = acceleration
        self.friction = friction
        self.max_speed = max_speed

        self.velocity_x = 0.0

    def update(self, direction):
        if direction != 0:
            self.velocity_x += direction * self.acceleration

            if self.velocity_x > self.max_speed:
                self.velocity_x = self.max_speed
            elif self.velocity_x < -self.max_speed:
                self.velocity_x = -self.max_speed
        else:
            self.apply_friction()

    def apply_friction(self):
        if self.velocity_x > 0:
            self.velocity_x -= self.friction
            if self.velocity_x < 0:
                self.velocity_x = 0

        elif self.velocity_x < 0:
            self.velocity_x += self.friction
            if self.velocity_x > 0:
                self.velocity_x = 0

    def stop(self):
        self.velocity_x = 0.0