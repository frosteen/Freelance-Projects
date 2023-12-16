class Device:
    total = 0

    def __init__(self, name, address, position):
        self.name = name
        self.address = address
        self.position = position
        Device.total = Device.total + 1


class Reader(Device):
    total = 0

    def __init__(self, name, address, position, color="orange", A=-32, n=2):
        super().__init__(name, address, position)
        self.color = color
        self.A = A
        self.n = n
        Reader.total = Reader.total + 1


class Tag(Device):
    total = 0

    def __init__(self, name, address, position, color="green"):
        super().__init__(name, address, position)
        self.linked_readers_rssi = {}
        self.linked_readers_kalman_filter = {}
        self.linked_readers_filtered_rssi = {}
        self.linked_tags_distance = {}
        self.color = color
        Tag.total = Tag.total + 1

    def reset_linked_readers_rssi(self):
        self.linked_readers_rssi = {}

    def reset_linked_readers_kalman_filter(self):
        self.linked_readers_kalman_filter = {}

    def reset_linked_readers_filtered_rssi(self):
        self.linked_readers_filtered_rssi = {}

    def reset_linked_tags_distance(self):
        self.linked_tags_distance = {}
