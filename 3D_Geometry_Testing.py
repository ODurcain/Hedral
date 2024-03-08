import unittest
from ThreeD_Geometry import calc_bounding_box, rotate_mesh_logic, move_mesh_logic, is_convex_logic

class TestBoundingBox(unittest.TestCase):
    def test_calc_bounding_box_with_points(self):
        # Test with non-empty points list
        points = [(1, 2, 3), (4, 5, 6), (7, 8, 9)]
        min_point, max_point = calc_bounding_box(points)
        self.assertEqual(min_point, (1, 2, 3))
        self.assertEqual(max_point, (7, 8, 9))

    def test_calc_bounding_box_with_single_point(self):
        # Test with a single point
        points = [(0, 0, 0)]
        min_point, max_point = calc_bounding_box(points)
        self.assertEqual(min_point, (0, 0, 0))
        self.assertEqual(max_point, (0, 0, 0))

    def test_calc_bounding_box_with_empty_list(self):
        # Test with an empty points list
        points = []
        min_point, max_point = calc_bounding_box(points)
        self.assertIsNone(min_point)
        self.assertIsNone(max_point)

    def test_calc_bounding_box_with_unit_cube(self):
        # Test with a unit cube
        points = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
        min_point, max_point = calc_bounding_box(points)
        self.assertEqual(min_point, (0, 0, 0))
        self.assertEqual(max_point, (1, 1, 1))

    def test_calc_bounding_box_with_negative_values(self):
        # Test with negative values
        points = [(-1, -2, -3), (4, 5, 6), (7, 8, 9)]
        min_point, max_point = calc_bounding_box(points)
        self.assertEqual(min_point, (-1, -2, -3))
        self.assertEqual(max_point, (7, 8, 9))

    def test_calc_bounding_box_with_float_values(self):
        # Test with floating-point values
        points = [(1.5, 2.5, 3.5), (4.75, 5.25, 6.75), (7.125, 8.625, 9.875)]
        min_point, max_point = calc_bounding_box(points)
        self.assertEqual(min_point, (1.5, 2.5, 3.5))
        self.assertEqual(max_point, (7.125, 8.625, 9.875))

    def test_calc_bounding_box_with_mixed_values(self):
        # Test with mixed integer and floating-point values
        points = [(1, 2, 3), (4.75, 5.25, 6.75), (-7, -8, -9)]
        min_point, max_point = calc_bounding_box(points)
        self.assertEqual(min_point, (-7, -8, -9))
        self.assertEqual(max_point, (4.75, 5.25, 6.75))

# This emphasized something interesting. The order in which the matrices are being rotated
# https://www.mathforengineers.com/math-calculators/3D-point-rotation-calculator.html
class TestRotateMesh(unittest.TestCase):
    def test_rotate_mesh_X_axis(self):
        # Test rotation around X axis
        mesh = [(1, 2, 3), (4, 5, 6), (7, 8, 9)]
        rotated_mesh = rotate_mesh_logic(mesh, 90, 'X')
        expected_rotated_mesh = [(1, -3, 2), (4, -6, 5), (7, -9, 8)]
        for i in range(len(rotated_mesh)):
            for j in range(len(rotated_mesh[i])):
                self.assertAlmostEqual(rotated_mesh[i][j], expected_rotated_mesh[i][j], delta=0.0001)
 
    def test_rotate_mesh_Y_axis(self):
        # Test rotation around Y axis
        mesh = [(1, 2, 3), (4, 5, 6), (7, 8, 9)]
        rotated_mesh = rotate_mesh_logic(mesh, 90, 'Y')
        expected_rotated_mesh = [(3, 2, -1), (6, 5, -4), (9, 8, -7)]
        for i in range(len(rotated_mesh)):
            for j in range(len(rotated_mesh[i])):
                self.assertAlmostEqual(rotated_mesh[i][j], expected_rotated_mesh[i][j], delta=0.0001)
 
    def test_rotate_mesh_Z_axis(self):
        # Test rotation around Z axis
        mesh = [(1, 2, 3), (4, 5, 6), (7, 8, 9)]
        rotated_mesh = rotate_mesh_logic(mesh, 90, 'Z')
        expected_rotated_mesh = [(-2, 1, 3), (-5, 4, 6), (-8, 7, 9)]
        for i in range(len(rotated_mesh)):
            for j in range(len(rotated_mesh[i])):
                self.assertAlmostEqual(rotated_mesh[i][j], expected_rotated_mesh[i][j], delta=0.0001)
 
    def test_rotate_mesh_XY_plane(self):
        # Test rotation around XY plane
        mesh = [(1, 2, 3), (4, 5, 6), (7, 8, 9)]
        rotated_mesh = rotate_mesh_logic(mesh, 90, 'XY')
        expected_rotated_mesh = [(3, 1, 2), (6, 4, 5), (9, 7, 8)]
        for i in range(len(rotated_mesh)):
            for j in range(len(rotated_mesh[i])):
                self.assertAlmostEqual(rotated_mesh[i][j], expected_rotated_mesh[i][j], delta=0.0001)
 
    def test_rotate_mesh_XZ_plane(self):
        # Test rotation around XZ plane
        mesh = [(1, 2, 3), (4, 5, 6), (7, 8, 9)]
        rotated_mesh = rotate_mesh_logic(mesh, 90, 'XZ')
        expected_rotated_mesh = [(-2, -3, 1), (-5, -6, 4), (-8, -9, 7)]
        for i in range(len(rotated_mesh)):
            for j in range(len(rotated_mesh[i])):
                self.assertAlmostEqual(rotated_mesh[i][j], expected_rotated_mesh[i][j], delta=0.0001)
   
    def test_rotate_mesh_YZ_plane(self):
        # Test rotation around YZ plane
        mesh = [(1, 2, 3), (4, 5, 6), (7, 8, 9)]
        rotated_mesh = rotate_mesh_logic(mesh, 90, 'YZ')
        expected_rotated_mesh = [(3, 1, 2), (6, 4, 5), (9, 7, 8)]
        for i in range(len(rotated_mesh)):
            for j in range(len(rotated_mesh[i])):
                self.assertAlmostEqual(rotated_mesh[i][j], expected_rotated_mesh[i][j], delta=0.0001)

    def test_rotate_mesh_with_negative_values(self):
        mesh = [(-1, -2, -3), (4, 5, 6), (7, 8, 9)]
        rotated_mesh = rotate_mesh_logic(mesh, -90, 'X')
        expected_rotated_mesh = [(-1, -3, 2), (4, 6, -5), (7, 9, -8)]
        for i in range(len(rotated_mesh)):
            for j in range(len(rotated_mesh[i])):
                self.assertAlmostEqual(rotated_mesh[i][j], expected_rotated_mesh[i][j], delta=0.0001)

    def test_rotate_mesh_with_float_values(self):
        mesh = [(1.5, 2.5, 3.5), (4.75, 5.25, 6.75), (7.125, 8.625, 9.875)]
        rotated_mesh = rotate_mesh_logic(mesh, 45.5, 'Z')
        expected_rotated_mesh = [(-0.7318, 2.8221, 3.5),
                                 (-0.4152, 7.0677, 6.75),
                                 (-1.1578, 11.1272, 9.875)]
        # print("\nActual rotated mesh:")
        # for point in rotated_mesh:
        #     print(point)
        # print("\nExpected rotated mesh:")
        # for point in expected_rotated_mesh:
        #     print(point)
        for i in range(len(rotated_mesh)):
            for j in range(len(rotated_mesh[i])):
                self.assertAlmostEqual(rotated_mesh[i][j], expected_rotated_mesh[i][j], delta=0.0001)

    def test_rotate_mesh_with_mixed_values(self):
        mesh = [(1, 2, 3), (4.75, 5.25, 6.75), (-7, -8, -9)]
        rotated_mesh = rotate_mesh_logic(mesh, 45.5, 'Z')
        expected_rotated_mesh = [(-0.7256, 2.1151, 3.0),
                                 (-0.4152, 7.0677, 6.75),
                                 (0.7996, -10.6000, -9.0)]
        # print("\nActual rotated mesh:")
        # for point in rotated_mesh:
        #     print(point)
        # print("\nExpected rotated mesh:")
        # for point in expected_rotated_mesh:
        #     print(point)
        for i in range(len(rotated_mesh)):
            for j in range(len(rotated_mesh[i])):
                self.assertAlmostEqual(rotated_mesh[i][j], expected_rotated_mesh[i][j], delta=0.0001)
             
    def test_rotate_mesh_empty_mesh(self):
        # Test rotation of an empty mesh
        mesh = []
        rotated_mesh = rotate_mesh_logic(mesh, 90, 'X')
        self.assertIsNone(rotated_mesh)

class TestMoveMesh(unittest.TestCase):
    def test_move_mesh_with_valid_mesh(self):
        # Test moving a valid mesh
        mesh = [(1, 2, 3), (4, 5, 6), (7, 8, 9)]
        moved_mesh = move_mesh_logic(mesh, 1, 2, 3)
        expected_moved_mesh = [(2, 4, 6), (5, 7, 9), (8, 10, 12)]
        self.assertEqual(moved_mesh, expected_moved_mesh)

    def test_move_mesh_with_empty_mesh(self):
        # Test moving an empty mesh
        mesh = []
        moved_mesh = move_mesh_logic(mesh, 1, 2, 3)
        self.assertIsNone(moved_mesh, None)

    def test_move_mesh_with_negative_values(self):
        # Test moving a mesh with negative values
        mesh = [(1, 2, 3), (-4, -5, -6), (7, 8, 9)]
        moved_mesh = move_mesh_logic(mesh, -1, -2, -3)
        expected_moved_mesh = [(0, 0, 0), (-5, -7, -9), (6, 6, 6)]
        self.assertEqual(moved_mesh, expected_moved_mesh)

    def test_move_mesh_with_float_values(self):
        # Test moving a mesh with floating-point values
        mesh = [(1.5, 2.5, 3.5), (4.75, 5.25, 6.75), (7.125, 8.625, 9.875)]
        moved_mesh = move_mesh_logic(mesh, 1.5, 2.5, 3.5)
        expected_moved_mesh = [(3.0, 5.0, 7.0), (6.25, 7.75, 10.25), (8.625, 11.125, 13.375)]
        for i in range(len(moved_mesh)):
            for j in range(len(moved_mesh[i])):
                self.assertAlmostEqual(moved_mesh[i][j], expected_moved_mesh[i][j], delta=0.0001)

    def test_move_mesh_with_mixed_values(self):
        # Test moving a mesh with mixed integer and floating-point values
        mesh = [(1, 2, 3), (4.75, 5.25, 6.75), (-7, -8, -9)]
        moved_mesh = move_mesh_logic(mesh, 1.5, -2.5, 3)
        expected_moved_mesh = [(2.5, -0.5, 6), (6.25, 2.75, 9.75), (-5.5, -10.5, -6)]
        for i in range(len(moved_mesh)):
            for j in range(len(moved_mesh[i])):
                self.assertAlmostEqual(moved_mesh[i][j], expected_moved_mesh[i][j], delta=0.0001)

class TestIsConvex(unittest.TestCase):
    def test_is_convex_with_convex_points(self):
        # Test with convex points
        convex_points = [(0, 0, 0), (0, 1, 0), (1, 1, 0), (1, 0, 0)]
        self.assertEqual(True, is_convex_logic(convex_points))

    def test_is_convex_with_concave_points(self):
        # Test with concave points
        concave_points = [(0, 0, 0), (2, 0, 0), (2, 2, 0), (1, 3, 0), (0, 2, 0)]
        self.assertEqual(False, is_convex_logic(concave_points))

    def test_is_convex_with_negative_points(self):
        # Test with negative points
        negative_points = [(0, 0, 0), (-1, -1, 0), (-1, 0, 0), (0, -1, 0)]
        self.assertEqual(True, is_convex_logic(negative_points))

    def test_is_convex_with_float_points(self):
        # Test with float points
        float_points = [(0.5, 0.5, 0), (0.5, 1.5, 0), (1.5, 1.5, 0), (1.5, 0.5, 0)]
        self.assertEqual(True, is_convex_logic(float_points))

    def test_is_convex_with_mixed_points(self):
        # Test with mixed integer and float points
        mixed_points = [(0, 0, 0), (-1.5, -1.5, 0), (-1, 0, 0), (0, -1, 0)]
        self.assertEqual(True, is_convex_logic(mixed_points))

    def test_is_convex_with_concave_negative_points(self):
        # Test with concave negative points
        concave_negative_points = [(0, 0, 0), (-2, 0, 0), (-2, -2, 0), (-1, -1, 0), (0, -2, 0)]
        self.assertEqual(False, is_convex_logic(concave_negative_points))

    def test_is_convex_with_concave_float_points(self):
        # Test with concave float points
        concave_float_points = [(0.5, 0.5, 0), (1.5, 0.5, 0), (1.5, -1.5, 0), (0.5, -1.5, 0), (-0.5, -0.5, 0)]
        self.assertEqual(False, is_convex_logic(concave_float_points))

    def test_is_convex_with_concave_mixed_points(self):
        # Test with concave mixed integer and float points
        concave_mixed_points = [(0, 0, 0), (2, 0, 0), (2, -2, 0), (1, -3, 0), (0, -2, 0), (-1.5, -1.5, 0)]
        self.assertEqual(False, is_convex_logic(concave_mixed_points))

    def test_is_convex_with_empty_points(self):
        # Test with empty points
        empty_points = []
        self.assertIsNone(is_convex_logic(empty_points))

if __name__ == '__main__':
    unittest.main()
