import unittest, os, sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from main.ThreeD_Geometry import (calc_bounding_box, rotate_mesh_logic, 
                                  move_mesh_logic, is_convex_logic, 
                                  scale_mesh_logic,reflect_mesh_logic,shear_mesh_logic)

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
        # Test with float values
        points = [(1.5, 2.5, 3.5), (4.75, 5.25, 6.75), (7.125, 8.625, 9.875)]
        min_point, max_point = calc_bounding_box(points)
        self.assertEqual(min_point, (1.5, 2.5, 3.5))
        self.assertEqual(max_point, (7.125, 8.625, 9.875))

    def test_calc_bounding_box_with_mixed_values(self):
        # Test with mixed integer and float values
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
        # Test moving a mesh with float values
        mesh = [(1.5, 2.5, 3.5), (4.75, 5.25, 6.75), (7.125, 8.625, 9.875)]
        moved_mesh = move_mesh_logic(mesh, 1.5, 2.5, 3.5)
        expected_moved_mesh = [(3.0, 5.0, 7.0), (6.25, 7.75, 10.25), (8.625, 11.125, 13.375)]
        for i in range(len(moved_mesh)):
            for j in range(len(moved_mesh[i])):
                self.assertAlmostEqual(moved_mesh[i][j], expected_moved_mesh[i][j], delta=0.0001)

    def test_move_mesh_with_mixed_values(self):
        # Test moving a mesh with mixed integer and float values
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

class TestScale(unittest.TestCase):
    def test_scale_all_coordinates(self):
        # Define some test points
        points = [(1.0, 2.0, 3.0), (4.0, 5.0, 6.0), (7.0, 8.0, 9.0)]
        
        # Test scaling where all x, y, z factors are non-zero
        scaled_mesh = scale_mesh_logic(points, 2.0, 0.5, 3.0)
        
        # Expected result after scaling
        expected_result = [(2.0, 1.0, 9.0), (8.0, 2.5, 18.0), (14.0, 4.0, 27.0)]
        
        # Compare the scaled mesh with the expected result
        self.assertEqual(scaled_mesh, expected_result)

    def test_scale_with_zero_factors(self):
        # Define some test points
        points = [(1.0, 2.0, 3.0), (4.0, 5.0, 6.0), (7.0, 8.0, 9.0)]
        
        # Test scaling where one or more factors are zero
        scaled_mesh = scale_mesh_logic(points, 0.0, 1.0, 3.0)
        
        # Expected result after scaling
        expected_result = [(0.0, 2.0, 9.0), (0.0, 5.0, 18.0), (0.0, 8.0, 27.0)]
        
        # Compare the scaled mesh with the expected result
        self.assertEqual(scaled_mesh, expected_result)

    def test_empty_input(self):
        # Test with empty input
        scaled_mesh = scale_mesh_logic([], 2.0, 0.5, 3.0)
        
        # Expected result should be None
        self.assertIsNone(scaled_mesh)

class TestReflect(unittest.TestCase):
    def test_reflect_xy(self):
        # Define some test points
        points = [(1.0, 2.0, 3.0), (4.0, 5.0, 6.0), (7.0, 8.0, 9.0)]
        
        # Test reflection about the XY plane
        reflected_mesh = reflect_mesh_logic(points, 'XY')
        
        # Expected result after reflection
        expected_result = [(1.0, 2.0, -3.0), (4.0, 5.0, -6.0), (7.0, 8.0, -9.0)]
        
        # Compare the reflected mesh with the expected result
        self.assertEqual(reflected_mesh, expected_result)

    def test_reflect_xz(self):
        # Define some test points
        points = [(1.0, 2.0, 3.0), (4.0, 5.0, 6.0), (7.0, 8.0, 9.0)]
        
        # Test reflection about the XZ plane
        reflected_mesh = reflect_mesh_logic(points, 'XZ')
        
        # Expected result after reflection
        expected_result = [(1.0, -2.0, 3.0), (4.0, -5.0, 6.0), (7.0, -8.0, 9.0)]
        
        # Compare the reflected mesh with the expected result
        self.assertEqual(reflected_mesh, expected_result)

    def test_reflect_yz(self):
        # Define some test points
        points = [(1.0, 2.0, 3.0), (4.0, 5.0, 6.0), (7.0, 8.0, 9.0)]
        
        # Test reflection about the YZ plane
        reflected_mesh = reflect_mesh_logic(points, 'YZ')
        
        # Expected result after reflection
        expected_result = [(-1.0, 2.0, 3.0), (-4.0, 5.0, 6.0), (-7.0, 8.0, 9.0)]
        
        # Compare the reflected mesh with the expected result
        self.assertEqual(reflected_mesh, expected_result)

    def test_invalid_axis(self):
        # Define some test points
        points = [(1.0, 2.0, 3.0), (4.0, 5.0, 6.0), (7.0, 8.0, 9.0)]
        
        # Test reflection with an invalid axis
        with self.assertRaises(ValueError):
            reflect_mesh_logic(points, 'XYZ')

    def test_empty_input(self):
        # Test with empty input
        reflected_mesh = reflect_mesh_logic([], 'XY')
        
        # Expected result should be None
        self.assertIsNone(reflected_mesh)

# shear logic is weird 
class TestShear(unittest.TestCase):
    def test_shear_x(self):
        # Define some test points
        points = [(1.0, 2.0, 3.0), (4.0, 5.0, 6.0), (7.0, 8.0, 9.0)]
        
        # Test shearing along the X-axis
        sheared_mesh = shear_mesh_logic(points, 3, 2, 8, 'X')
        
        # Expected result after shearing along X-axis
        expected_result = [(1,4,11), (4,13,38), (7,22,65)]  # Updated
        
        # Compare the sheared mesh with the expected result
        self.assertEqual(sheared_mesh, expected_result)

    def test_shear_y(self):
        # Define some test points
        points = [(1.0, 2.0, 3.0), (4.0, 5.0, 6.0), (7.0, 8.0, 9.0)]
        
        # Test shearing along the Y-axis
        sheared_mesh = shear_mesh_logic(points, 3, 2, 8, 'Y')
        
        # Expected result after shearing along Y-axis
        expected_result = [(7,2,19), (19,5,46), (31,8,73)]  # Updated
        
        # Compare the sheared mesh with the expected result
        self.assertEqual(sheared_mesh, expected_result)

    def test_shear_z(self):
        # Define some test points
        points = [(1.0, 2.0, 3.0), (4.0, 5.0, 6.0), (7.0, 8.0, 9.0)]
        
        # Test shearing along the Z-axis
        sheared_mesh = shear_mesh_logic(points, 3, 2, 8, 'Z')
        
        # Expected result after shearing along Z-axis
        expected_result = [(10,8,3), (22,17,6), (34,26,9)]  # Updated
        
        # Compare the sheared mesh with the expected result
        self.assertEqual(sheared_mesh, expected_result)

    def test_shear_xy(self):
        # Define some test points
        points = [(1.0, 2.0, 3.0), (4.0, 5.0, 6.0), (7.0, 8.0, 9.0)]
        
        # Test shearing along the XY-plane
        sheared_mesh = shear_mesh_logic(points, 3, 2, 8, 'XY')
        
        # Expected result after shearing along XY-plane
        expected_result = [(7,16,75), (19,43,198), (31,70,321)]  # Updated
        
        # Compare the sheared mesh with the expected result
        self.assertEqual(sheared_mesh, expected_result)

    def test_shear_xz(self):
        # Define some test points
        points = [(1.0, 2.0, 3.0), (4.0, 5.0, 6.0), (7.0, 8.0, 9.0)]
        
        # Test shearing along the XZ-plane
        sheared_mesh = shear_mesh_logic(points, 3, 2, 8, 'XZ')
        
        # Expected result after shearing along XZ-plane
        expected_result = [(10,28,83), (22,61,182), (34,94,281)]  # Updated
        
        # Compare the sheared mesh with the expected result
        self.assertEqual(sheared_mesh, expected_result)

    def test_shear_yz(self):
        # Define some test points
        points = [(1.0, 2.0, 3.0), (4.0, 5.0, 6.0), (7.0, 8.0, 9.0)]
        
        # Test shearing along the YZ-plane
        sheared_mesh = shear_mesh_logic(points, 3, 2, 8, 'YZ')
        
        # Expected result after shearing along YZ-plane
        expected_result = [(34,8,67), (73,17,142), (112,26,217)]  # Updated
        
        # Compare the sheared mesh with the expected result
        self.assertEqual(sheared_mesh, expected_result)

    def test_invalid_axis(self):
        # Define some test points
        points = [(1.0, 2.0, 3.0), (4.0, 5.0, 6.0), (7.0, 8.0, 9.0)]
        
        # Test shearing with an invalid axis
        with self.assertRaises(ValueError):
            shear_mesh_logic(points, 0.5, 0.5, 0.0, 'XYZ')

    def test_empty_input(self):
        # Test with empty input
        sheared_mesh = shear_mesh_logic([], 0.5, 0.5, 0.0, 'XY')
        
        # Expected result should be None
        self.assertIsNone(sheared_mesh)

if __name__ == '__main__':
    unittest.main()
