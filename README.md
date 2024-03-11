# Hedral: Geometric Computation

Jump to bottom for some development notes.

## Run:
1. Clone the repo to a directory of your choice https://github.com/ODurcain/Hedral/ 
2. Navigate to ../Hedral directory. 
3. run 
```
docker-compose build
docker-compose up
```
6. Checking Running on `ip:port` (Assume `ip:port` = `localhost:5000`, but may be machine dependant)
Type `ip:port` into browser, or CTRL + ‘click’ `http://ip:port`
7. Begin to utilize the implemented functions below.

## Smallest Bounding Box:
1. Put in an array of points in the following format (copy and paste the cell to see a sample run):
   
| Sample |
| ------ |
| 1,2,3  |
| 4,5,6  |
| 7,8,9  |

2. Press the “Calculate” button
3. The output is the minimum and maximum points which create a bounding box extrapolated from said points:

`Output: {"The bounding box is from min_point":[1,2,3],"to max_point":[7,8,9]}`

## Rotate Mesh:
1. Put in an array of points in the following format (copy and paste the cell to see a sample run): 

| Sample |
| ------ |
| 1,2,3  |
| 4,5,6  |
| 7,8,9  |


2. Set the degrees you want. Can set it to any number and it will parse anything over 360 correctly (sample below):
   
| Degree |
| ------ |
| 45     |

3. Select the axis in which you want the mesh rotated from the drop down menu (sample done with X).
4. Press the “Rotate” button.
5. The output will be the new coordinates of the mesh after rotating:

`Output: {"rotated_mesh":[[1,-0.7071067811865472,3.5355339059327378],[4,-0.707106781186547,7.778174593052023],[7,-0.707106781186547,12.020815280171309]]}`
	
## Move Mesh:
1. Put in an array of points in the following format (copy and paste the cell to see a sample run): 

| Sample |
| ------ |
| 1,2,3  |
| 4,5,6  |
| 7,8,9  |

2. Set the x, y, and z values you want to move the polygon by (set all 3 boxes to samples):
   
|    X   |   Y   |   Z   |
| ------ | ----- | ----- |
|    4   |   4   |   4   |

3. Press the “Move” button.
4. The output will be the new coordinates of the mesh after moving:

`Output: {"moved_mesh":[[5,6,7],[8,9,10],[11,12,13]]}`

## Check Convex:
1. Put in an array of points in the following format (copy and paste the cells to see sample runs):

| Convex  |
| ------- |
| 0,0,0   |
| 1,0,0   |
| 1,1,0   |
| 0,1,0   |
|`Output: {"convex":true}`|

| Not Convex  |
| ------- |
| 0,0,0   |
| 3,0,0   |
| 3,3,0   |
| 2,2,0   |
| 1,3,0   |
| 0,2,0   |
|`Output: {"convex":false}`|

2. Press the “Convex?” button and it will respond true if the polygon is convex and false if it is concave.

## Testing

```
python3 3D_Geometry_Testing.py
```

### Notes:

* Setup complete. This was done in WSL as Windows was not recognizing Flask.
* Setup steps end at a relevant point for someone to run the program.
* This setup guide is meant to be ambiguous to allow for both running an existing environment and setting up a new environment.
* Convex hull was the most complicated. Gift wrapping did not work, so I eventually switched to Graham scan. Thanks to this wikipedia page helping me easily see all of my options for algorithms. https://en.wikipedia.org/wiki/Convex_hull_algorithms
* I would love to revisit this and attempt Chan’s algorithm, but seeing as I couldn’t get gift wrapping to work I’m not too positive. I did read that the way that the gift wrapping algorithm works has flaws, so maybe that’s why I was getting incorrect readings. 
* I accidentally lost the Gift wrapping algorithm code, so maybe it wasn’t meant to be. 
* When doing dual axis rotation there are different order in which you can rotate the axis and I used an online calculator to figure out the order in which python chooses to do it. It has a tendency to go Z > Y > X as I found through testing.
* Move mesh and bounding box were straightforward with NumPy library and basic arithmetic operations.
* `ThreeD_geometry_with_Plotting.py` can be disregarded. It does work and will output a 3D plot with points, but it's not where I want it to be. It also has the beginnings of scalar, shear, reflection, and rotate/move simultaneously.
* `index_with_plotting_precision.html` can also be disregarded for the time being. This handles the aforementioned plotting and also has the beginnings of adjustable precision (I made the assumption it was referencing significant figures).
* I have made the Docker container as streamlined as possible. The one thing that I was unable to do was open a web browser from inside of a Docker container. I tried everything I could find documentation wise and various tips & tricks, but it seems a genuine limitation of Docker.
* I actually found an error in [geeksforgeeks](https://www.geeksforgeeks.org/computer-graphics-3d-shearing-transformation/) math for the end sheared function as their B point is 8,10,2, but the math and my program gave me 4,10,2

(Admin level. Jump to run for relevant information)
Setup Steps:
1. Go to the directory containing the project:
```
Python -m venv <env_name>
```
- Activate virtual env
- Windows:
  ```
  <env_name>\Scripts\activate
  ```
- Mac/Linux:
  ```
  source <env_name>/bin/activate
  ```
  ```
  pip install Flask Flask-sqlalchemy
  pip install matplotlib
  pip install scipy
  pip install numpy
  ```
2. From here the system should be setup
