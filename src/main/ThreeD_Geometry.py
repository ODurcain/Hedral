## Geometric Functions Calculator
## Created 3/7/2024

from flask import Flask, request, jsonify, render_template
import numpy as np
# For bounding box
from typing import List, Tuple
# for rotation. may import all of math for scalar stuff
from math import cos, sin, radians, sqrt, pi, acos

app=Flask(__name__, template_folder='../../templates')

# I didn't know this was a hard requirement for Flask and I was stuck for an hour with a 404 error
@app.route('/')
def index():
    return render_template('index.html')

# smallest box logic
def calc_bounding_box(points: List[Tuple[float,float,float]]) -> Tuple[Tuple[float,float,float], Tuple[float,float,float]]:
    if not points:
        return None, None
    min_points = np.min(points, axis=0)
    max_points = np.max(points, axis=0)
    return tuple(min_points), tuple(max_points)

# smallest box connection to flask
@app.route('/bounding_box', methods=['POST'])
def bounding_box():
    try:
        points = request.json['points']
        points = np.array(points).astype(float).tolist()
        min_points, max_points=calc_bounding_box(points)
        return jsonify({'The bounding box is from min_point': min_points, 'to max_point': max_points}), 200
    except KeyError as e:
        invalid_parameter = str(e)
        return jsonify({'error': f'Invalid input format: missing parameter "{invalid_parameter}"'}), 400
    
# rotaion of a 3D mesh logic    
def rotate_mesh_logic(mesh: List[Tuple[float,float,float]], 
                angle: float, axis: str) -> Tuple[Tuple[float,float,float], 
                                                  Tuple[float,float,float]]:
    if not mesh:
        return None
    # converting to raidians
    angle_radians = radians(angle)

    x_rotation_matrix=np.array([
        [1,0,0],
        [0, cos(angle_radians), -sin(angle_radians)],
        [0, sin(angle_radians), cos(angle_radians)]])
    
    y_rotation_matrix=np.array([
        [cos(angle_radians), 0,sin(angle_radians)],
        [0,1,0],
        [-sin(angle_radians),0, cos(angle_radians)]])
    
    z_rotation_matrix=np.array([
        [cos(angle_radians), -sin(angle_radians),0],
        [sin(angle_radians),cos(angle_radians),0],
        [0,0,1]])
    
    # logic was pulled from this video about OpenGL https://www.youtube.com/watch?v=AgcryeeIhew
    if axis =='X':
        rotation_matrix=x_rotation_matrix

    elif axis == 'Y':
        rotation_matrix=y_rotation_matrix

    elif axis == 'Z':
        rotation_matrix=z_rotation_matrix

    # for 2 dimensional rotation
    elif axis=='XY':
        rotation_matrix=np.dot(x_rotation_matrix, y_rotation_matrix)

    elif axis=='XZ':
        rotation_matrix=np.dot(x_rotation_matrix, z_rotation_matrix)

    elif axis=='YZ':
        rotation_matrix=np.dot(y_rotation_matrix, z_rotation_matrix)

    else:
        raise ValueError("Invalid. must be X, Y, Z, XY, XZ, or YZ")
    
    rotated_mesh=[]
    for point in mesh:
        rotated_point=np.dot(rotation_matrix, point)
        rotated_mesh.append(tuple(rotated_point))

    return rotated_mesh
        
# rotation of a 3D mesh connection to flask
@app.route('/rotate_mesh', methods=['POST'])
def rotate_mesh_endpoint():
    try:
        data=request.get_json()
        mesh=data['points'] # make sure you're not looking for nonexistent data
        angle=data['angle']
        axis=data['axis']
        rotated_mesh = rotate_mesh_logic(mesh, angle, axis)
        return jsonify({'rotated_mesh': rotated_mesh}), 200
    except KeyError:
        return jsonify({'error': 'Invalid Input Format'}), 400

def move_mesh_logic(points: List[Tuple[float,float,float]], 
                x: float, y: float, z: float) -> List[Tuple[float,float,float]]:
    if not points:
        return None
    moved_mesh=[]
    for point in points:
        moved_point=(point[0]+x, point[1]+y, point[2]+z)
        moved_mesh.append(moved_point)
    return moved_mesh

# movement of a 3D mesh connection to a flaks
@app.route('/move_mesh', methods=['POST'])
def move_mesh_endpoint():
    try:
        data=request.get_json()
        mesh=data['points']
        xDir=data['xDirectionMove']
        yDir=data['yDirectionMove']
        zDir=data['zDirectionMove']
        moved_mesh=move_mesh_logic(mesh, xDir, yDir, zDir)
        return jsonify({'moved_mesh': moved_mesh}), 200
    except KeyError as e:
        invalid_parameter = str(e)
        return jsonify({'error': f'Invalid input format: missing parameter "{invalid_parameter}"'}), 400
    
def orientation(p: Tuple[float, float, float], q: Tuple[float, float, float], r: Tuple[float, float, float]) -> int:
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    if val == 0:
        return 0  # collinear
    return 1 if val > 0 else 2  # c or ccw

def graham_scan(points: List[Tuple[float, float, float]]) -> List[Tuple[float, float, float]]:
    sorted_points = sorted(points, key=lambda p: (p[0], p[1], p[2]))
    
    # Function to determine the orientation of three points
    def orientation(p1, p2, p3):
        val = (p2[1] - p1[1]) * (p3[0] - p2[0]) - (p3[1] - p2[1]) * (p2[0] - p1[0])
        if val == 0:
            return 0  # collinear
        elif val > 0:
            return 1  # cw
        else:
            return 2  # ccw
    
    stack = []
    stack.append(sorted_points[0])
    stack.append(sorted_points[1])
    stack.append(sorted_points[2])
    
    # rest of the points
    for i in range(3, len(sorted_points)):
        # remove points from the stack while the orientation of the last three points is not counterclockwise
        while len(stack) > 1 and orientation(stack[-2], stack[-1], sorted_points[i]) != 2:
            stack.pop()
        stack.append(sorted_points[i])
    
    return stack

def is_convex_logic(points: List[Tuple[float, float, float]]) -> bool:

    if not points:
        return None
    convex_hull = graham_scan(points)
    
    # check if the number of points in the convex hull is equal to the number of points in the original polygon
    return len(convex_hull) == len(points)

@app.route('/is_convex', methods=['POST'])
def is_convex():
    try:
        data=request.get_json()
        mesh=data['points']
        convex=is_convex_logic(mesh)
        return jsonify({'convex': convex}), 200
    except KeyError:
        return jsonify({'error': 'Invalid input format'}), 400

def scale_mesh_logic(points: List[Tuple[float,float,float]], 
                     x: float, y: float, z: float) -> List[Tuple[float,float,float]]:
    if not points or x is None or y is None or z is None:
        return None
    
    # going to update later for precision. will most likely be a global variable
    epsilon=0.0001

    x= 1 if abs(x) < epsilon else x
    y= 1 if abs(y) < epsilon else y
    z= 1 if abs(z) < epsilon else z
    
    scaled_mesh = []
    for point in points:
        scaled_point = (point[0] * (x if point[0]==max(p[0] for p in points) else 1),
                        point[1] * (y if point[0]==max(p[1] for p in points) else 1), 
                        point[2] * (z if point[0]==max(p[2] for p in points) else 1))
        scaled_mesh.append(scaled_point)
    
    return scaled_mesh

# scaling of a 3D mesh connection to a flaks
@app.route('/scale_mesh', methods=['POST'])
def scale_mesh_endpoint():
    try:
        data=request.get_json()
        mesh=data['points']
        xDir=data['xDirectionScale']
        yDir=data['yDirectionScale']
        zDir=data['zDirectionScale']
        scaled_mesh=scale_mesh_logic(mesh, xDir, yDir, zDir)
        return jsonify({'scaled_mesh': scaled_mesh}), 200
    except KeyError as e:
        invalid_parameter = str(e)
        return jsonify({'error': f'Invalid input format: missing parameter "{invalid_parameter}"'}), 400
    
def reflect_mesh_logic(points: List[Tuple[float,float,float]], 
                       axisReflect: str) -> List[Tuple[float,float,float]]:
    if not points:
        return None
    
    xy_reflect_matrix = np.array([[1,0,0],
                                   [0,1,0],
                                   [0,0,-1]])
    xz_reflect_matrix = np.array([[1,0,0],
                                   [0,-1,0],
                                   [0,0,1]])
    yz_reflect_matrix = np.array([[-1,0,0],
                                   [0,1,0],
                                   [0,0,1]])
    
    if axisReflect == 'XY':
        reflect_matrix = xy_reflect_matrix
    elif axisReflect == 'XZ':
        reflect_matrix = xz_reflect_matrix
    elif axisReflect == 'YZ':
        reflect_matrix = yz_reflect_matrix
    else:
        raise ValueError("Invalid axis. Must be XY, XZ, or YZ")
    
    reflected_matrix = []
    for point in points:
        transformed_point = np.dot(reflect_matrix, point) 
        reflected_matrix.append(tuple(transformed_point.tolist()))

    return reflected_matrix

@app.route('/reflect_mesh', methods=['POST'])
def reflect_mesh_endpoint():
    try:
        data=request.get_json()
        mesh=data['points']
        axisReflect=data['axisReflect']
        reflected_mesh=reflect_mesh_logic(mesh, axisReflect)
        return jsonify({'reflected_mesh': reflected_mesh}), 200
    except KeyError as e:
        invalid_parameter = str(e)
        return jsonify({'error': f'Invalid input format: missing parameter "{invalid_parameter}"'}), 400

def shear_mesh_logic(points: List[Tuple[float,float,float]], 
                x: float, y: float, z: float, axisShear: str) -> List[Tuple[float,float,float]]:
    if not points:
        return None
    
    x_shear_matrix=np.array([[1,y,z],
                              [0,1,0],
                              [0,0,1]])
    y_shear_matrix=np.array([[1,0,0],
                              [x,1,z],
                              [0,0,1]])
    z_shear_matrix=np.array([[1,0,x],
                              [0,1,y],
                              [0,0,1]])
    
    if axisShear =='X':
        shear_matrix=x_shear_matrix

    elif axisShear == 'Y':
        shear_matrix=y_shear_matrix

    elif axisShear == 'Z':
        shear_matrix=z_shear_matrix

    # 2 directional shear
    elif axisShear=='XY':
        shear_matrix=np.dot(x_shear_matrix, y_shear_matrix)

    elif axisShear=='XZ':
        shear_matrix=np.dot(x_shear_matrix, z_shear_matrix)

    elif axisShear=='YZ':
        shear_matrix=np.dot(y_shear_matrix, z_shear_matrix)

    else:
        raise ValueError("Invalid. must be X, Y, Z, XY, XZ, or YZ")
    
    sheared_mesh=[]
    for point in points:
        transformed_point = np.dot(shear_matrix, point)
        sheared_mesh.append(transformed_point.tolist())

    return sheared_mesh

# movement of a 3D mesh connection to a flaks
@app.route('/shear_mesh', methods=['POST'])
def shear_mesh_endpoint():
    try:
        data=request.get_json()
        mesh=data['points']
        xDir=float(data['xDirectionShear'])
        yDir=float(data['yDirectionShear'])
        zDir=float(data['zDirectionShear'])
        axisShear=data['axisShear']
        sheared_mesh=shear_mesh_logic(mesh, xDir, yDir, zDir, axisShear)
        return jsonify({'sheared_mesh': sheared_mesh}), 200
    except KeyError as e:
        invalid_parameter = str(e)
        return jsonify({'error': f'Invalid input format: missing parameter "{invalid_parameter}"'}), 400

if __name__=="__main__":
    app.run(debug=True)