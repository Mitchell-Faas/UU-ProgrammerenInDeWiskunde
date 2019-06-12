class Rect:
    """A class of rectangles, to be used for rooms

    This class consists of rectangles at a certain position and of certain proportions. This class is used
    during map creation to procedurally place rooms.

    Parameters
    ----------
    x : int
        The horizontal coordinate of the top-left corner of the rectangle.
    y : int
        The vertical coordinate of the top-left corner of the rectangle.
    width : int
        The horizontal length of the rectangle, in number of tiles.
    height : int
        The vertical length of the rectangle, in number of tiles.

    """
    def __init__(self, x, y, width, height):
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height

    def center(self):
        """A function that calculates the center of a rectangle

        This function gives the coordinates of the center of an instance of the Rectangle class.
        """
        center_x = (self.x1 + self.x2) // 2
        center_y = (self.y1 + self.y2) // 2
        return center_x, center_y

    def intersects_with(self, other):
        """A function that checks whether two rectangles overlap

        This function checks whether two instances of the Rectangle class overlap. This is important during
        map creation, so we can avoid placing overlapping rooms.

        Parameters
        ----------
        other : :obj:`Rectangle`
            Another instance of the Rectangle class, of which we want to know whether it overlaps.
        """
        # returns true if this rectangle intersects with "other"
        intersect_bool = self.x1 <= other.x2 and \
                         self.x2 >= other.x1 and \
                         self.y1 <= other.y2 and \
                         self.y2 >= other.y1
        return intersect_bool
