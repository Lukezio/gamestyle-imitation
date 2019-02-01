"""All the functionalities for a point"""

class Point:
    """The point class"""

    def __init__(self, x, y):
        self.x_coordinate = x
        self.y_coordinate = y

    @staticmethod
    def get_top_left(point_1, point_2):
        """get top left point for any 2 points"""
        return Point(point_1.x_coordinate if point_1.x_coordinate < point_2.x_coordinate
                     else point_2.x,
                     point_1.y_coordinate if point_1.y_coordinate < point_2.y_coordinate
                     else point_2.y_coordinate)

    @staticmethod
    def get_bottom_right(point_1, point_2):
        """get bottom right point for any 2 points"""
        return Point(point_1.x_coordinate if point_1.x_coordinate > point_2.x_coordinate
                     else point_2.x,
                     point_1.y_coordinate if point_1.y_coordinate > point_2.y_coordinate
                     else point_2.y_coordinate)

    def __str__(self):
        """tostring"""
        return "x=" + str(self.x_coordinate) + ", y=" + str(self.y_coordinate)
