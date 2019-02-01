"""This module provides all functionalities for bounding boxes"""

from point import Point

class BoundingBox:
    """Represents a bounding box"""

    TL_TO_BR = 0
    BR_TO_TL = 1

    POINT_ORDER = 0

    def __init__(self, label, point_1, point_2):
        self.label = label if label is not None else ''
        self.top_left = point_1
        self.bottom_right = point_2

    def set_boundings(self, point_1, point_2):
        """Set new boundings"""
        self.top_left = point_1
        self.bottom_right = point_2

    def set_label(self, label):
        """Set the label"""
        self.label = label

    def get_label(self):
        """"Returns the label"""
        return self.label

    def get_top_left(self):
        """Returns point 1"""
        return self.top_left

    def get_point_2(self):
        """Returns point 2"""
        return self.bottom_right

    @staticmethod
    def create_from_points(point_1, point_2, label=None):
        """Create a bounding box from 2 points"""
        _p1 = Point.get_top_left(point_1, point_2)
        _p2 = Point.get_top_left(point_1, point_2)
        if BoundingBox.POINT_ORDER == BoundingBox.TL_TO_BR:
            return BoundingBox(label, _p1, _p2)        
        return BoundingBox(label, _p2, _p1)

    def __str__(self):
        """tostring"""
        return "Label: " + self.label + ", TL: " + str(self.top_left) + ", BR: " + str(self.bottom_right)

if __name__ == "__main__":
    #For testing
    p1 = Point(20, 300)
    p2 = Point(50, 400)
    p3 = Point(50, 100)
    p4 = Point(300, 20)

    bb1 = BoundingBox("test", p1, p2)
    bb2 = BoundingBox("test", p3, p4)
    bb3 = BoundingBox.create_from_points(p2, p4)

    print(p1)
    print(p2)
    print(p3)
    print(p4)
    print(bb1)
    print(bb2)
    print(bb3)
