class Rect:
    def __init__(self, x, y, width, height):
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height

    def center(self):
        """Calculates and returns the center coordinates of this rectangle"""
        center_x = (self.x1 + self.x2) // 2
        center_y = (self.y1 + self.y2) // 2
        return center_x, center_y

    def intersects_with(self, other):
        # returns true if this rectangle intersects with "other"
        intersect_bool = self.x1 <= other.x2 and \
                         self.x2 >= other.x1 and \
                         self.y1 <= other.y2 and \
                         self.y2 >= other.y1
        return intersect_bool
