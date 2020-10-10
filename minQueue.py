import queueObject


class MinQueue:
    arr = []

    def __init__(self):
        self.arr = []

    def insert(self, position, previous_position, distance):
        if len(self.arr) == 0:
            self.arr.append(queueObject.QueueObject(position, previous_position, distance))
            return
        i = 0
        while i < len(self.arr):
            if distance < self.arr[i].get_distance():
                break
            i = i + 1
        self.arr.insert(i, queueObject.QueueObject(position, previous_position, distance))

    def pop(self):
        obj = self.arr.pop(0)

        return obj.get_position() + obj.get_previous_position()
