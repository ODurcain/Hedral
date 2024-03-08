import unittest
from ThreeD_Geometry import calc_bounding_box, rotate_mesh_logic, move_mesh_logic, is_convex_logic

class TestBoundingBox(unittest.TestCase):
    def test_calc_bounding_box(self):
        points = [(1, 2, 3), (4, 5, 6), (7, 8, 9)]
        points2 = [(0,0,0)]
        min_point, max_point = calc_bounding_box(points)
        min_point2, max_point2 = calc_bounding_box(points2)
        self.assertEqual(min_point, (1, 2, 3))
        self.assertEqual(max_point, (7, 8, 9))
        self.assertEqual(min_point2, (0,0,0))
        self.assertEqual(max_point2, (0,0,0))

class TestRotateMesh(unittest.TestCase):
    def test_rotate_mesh_logic(self):
        mesh = [(1, 2, 3), (4, 5, 6), (7, 8, 9)]
        rotated_mesh = rotate_mesh_logic(mesh, 90, 'X')
        expected_rotated_mesh = [(1, -3, 2), (4, -6, 5), (7, -9, 8)]
        self.assertEqual(rotated_mesh, expected_rotated_mesh)

class TestMoveMesh(unittest.TestCase):
    def test_move_mesh_logic(self):
        mesh = [(1, 2, 3), (4, 5, 6), (7, 8, 9)]
        moved_mesh = move_mesh_logic(mesh, 1, 2, 3)
        expected_moved_mesh = [(2,4,6),(5,7,9),(8,10,12)]
        self.assertEqual(moved_mesh,expected_moved_mesh)

class TestIsConvex(unittest.TestCase):
    def test_is_convex_logic(self):
        convex_points = [(0, 0, 0), (0, 1, 0), (1, 1, 0), (1, 0, 0)]
        concave_points = [(0, 0, 0), (2, 0, 0), (2, 2, 0), (1, 3, 0), (0, 2, 0)]
        
        self.assertEqual(True, is_convex_logic(convex_points))
        self.assertEqual(False, is_convex_logic(concave_points))

if __name__ == '__main__':
    unittest.main()
