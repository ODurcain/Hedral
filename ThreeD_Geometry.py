##

from flask import Flask, request, jsonify, render_template
import numpy as np
# For bounding box
from typing import List, Tuple
# for rotation. may import all of math for scalar stuff
from math import cos, sin, radians

app=Flask(__name__)

# I didn't know this was a hard requirement for Flask and I was stuck for an hour with a 404 error
@app.route('/')
def index():
    return render_template('index.html')

# smallest box logic
def calc_bounding_box(points: List[Tuple[float,float,float]]) -> Tuple[Tuple[float,float,float], Tuple[float,float,float]]:
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
    except KeyError:
        return jsonify({'error': 'Invalid input format'}), 400
    
# rotaion of a 3D mesh logic    
def rotate_mesh_logic(mesh: List[Tuple[float,float,float]], 
                angle: float, axis: str) -> Tuple[Tuple[float,float,float], 
                                                  Tuple[float,float,float]]:
    # converting to raidans
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

    elif axis=='XY':
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
        return jsonify({'error': 'Invalid input format'}), 400

def move_mesh_logic(points: List[Tuple[float,float,float]], 
                x: float, y: float, z: float) -> Tuple[Tuple[float,float,float], 
                                                  Tuple[float,float,float]]:
    #points = np.array(points).astype(float).tolist()

    moved_mesh=[]
    for point in points:
        moved_point=(point[0]+x, point[1]+y, point[2]+z)
        moved_mesh.append(moved_point)

    return moved_mesh


@app.route('/move_mesh', methods=['POST'])
def move_mesh_endpoint():
    try:
        data=request.get_json()
        mesh=data['points']
        xDir=data['xDirection']
        yDir=data['yDirection']
        zDir=data['zDirection']
        moved_mesh=move_mesh_logic(mesh, xDir, yDir, zDir)
        return jsonify({'moved_mesh': moved_mesh}), 200
    except KeyError:
        return jsonify({'error': 'Invalid input format'}), 400

# def is_convex(points: List[Tuple[float,float,float]]) -> bool:
# @app.route('/is_convex', methods=['POST'])
# def is_convex():
#     try:
#     except KeyError:
#         return jsonify({'error': 'Invalid input format'}), 400

if __name__=="__main__":
    app.run(debug=True)