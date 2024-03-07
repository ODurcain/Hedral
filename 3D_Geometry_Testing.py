import unittest
import numpy as np

from ThreeD_Geometry import bounding_box

class TestBoundingBox(unittest.TestCase):
    def test_bounding_box(self):
        points = np.array([[1,2,3],
                           [3,4,5],
                           [7,8,9]])
        
        expected_res={'min_point': [1,2,3], 'max_point': [7,8,9]}

        res = bounding_box(points)

        self.assertEqual(res, expected_res)

if __name__ == '__main__':
    unittest.main()