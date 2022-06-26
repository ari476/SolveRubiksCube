class Point:
    """
    A class that represents a point in cartesian coordinate
    """
    def __init__(self, x, y):
        """Defines x and y variables"""
        self.x = x
        self.y = y

    def __iter__(self):
        yield self.x
        yield self.y

    def unpack(self):
        return self.x, self.y
