class QueueObject:
    position = ()
    previous_position = ()
    distance = 0

    def __init__(self, position, previous_position, distance):
        self.position = position
        self.previous_position = previous_position
        self.distance = distance

    def get_distance(self):
        return self.distance

    def get_previous_position(self):
        return self.previous_position

    def get_position(self):
        return self.position

