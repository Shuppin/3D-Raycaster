&nbsp;
<div align="center"><h1>3D Raycaster</h1></div>

Welcome to my implementation of a 3D raycasting engine! This program demonstrates the use of the [DDA raycasting algorithm](https://lodev.org/cgtutor/raycasting.html) to query a 2D world map based on the current position of the player, and draw a 3D representation (with textures!) of that map.

Also included is a small minimap that gives a 2D representation of exactly what the raycasting looks like, as well as where the player is in the world.

&nbsp;

## Demo

https://github.com/Shuppin/3D-Raycaster/assets/72602326/342fa55a-f70f-4cc4-9919-87165f1f5c54

&nbsp;

## Running the program

To run the program from source, follow these simple steps:

1. Open a terminal and clone the repo by running `git clone https://github.com/Shuppin/3D-Raycaster.git` in your terminal.
2. Enter the directory by running `cd 3D-Raycaster`
2. Install the required dependencies by running `pip install -r requirements.txt`. (Depending on your OS, you may need a C compiler installed as well)
3. Finally, run the program by executing `python src/main.py` in your terminal. 

That's it! You should now be able to play with this simple raycaster.

&nbsp;

## Controls

Use `WASD` to move and rotate the camera.

The `X` key will toggle the height of the walls, this feature is useful to visually explain that the raycasting is only being performed on a single row of pixels.

The `M` key will render the current frame with a slight delay per pixel, allowing you to see how to algorithm works in slow motion. You can increase/decrease this delay using the `[` and `]` keys.

&nbsp;

## Performance considerations

As you may have noticed, this project is programmed in Python, you may have also noticed that Python, is slow, very slow. Despite this program using highly efficient raycasting algorthims and fast graphics libraries, I was not able to get this program to run (with textures) at an acceptable speed. For this reason, I am planning on moving the project over to C as that is the native language of raylib, and is much faster.

&nbsp;

## Technical explaination

### Map
The map is stored as a 2D array of integers, each number either representing an empty space (0), or a colour (1-5)

### Camera

<img align="right" width="240" height="240" src="https://github.com/Shuppin/3D-Raycaster/assets/72602326/b0aeef8a-990e-408d-a12c-496abc14dd0b">
The camera is made up of a position, direction vector and a plane vector.

- (pos)ition is a simple x, y vector and is directly representative of the position on the map (i.e. 0,0 is the top left of the map and mapWidth, mapHeight is the bottom right of the map)
- (dir)ection is another x, y vector which represents, you guessed it, the direction of the camera. The magnitude of this vector also represents the focal length
- plane is another x,y vector and that represents the width of the camera plane. The camera plane defines how wide the field of view should be.

### DDA Raycasting Algorithm

I highly recommend watching [this](https://www.youtube.com/watch?v=NbSee-XM7WA) video explaining how the algorithm works.

The DDA Ray casting algorithm is a very an efficient way to render a scene on the screen. Instead of casting a ray for every individual pixel, we cast a ray for each column of pixels. This approach significantly reduces the amount of rays required.

### 3D Visualisation

As each ray travels, it intersects with the boundaries of the grid. At each intersection, we check the value of the corresponding grid cell. If this value is greater than 0, then we know we have hit a wall. Once this happens, we then calculate how tall the column of pixels at this intersection should be based on the distance traveled by the ray.

### Textures

I'm a true artist at heart, and all my love was poured into these textures (for about 10 minutes).

Textures are loaded from the `img` directory, resized to a specified size, and then stored as an array of RGBA tuples.

### Applying textures

When a ray collides with a wall, we determine the exact location of the collision and calculate the height of the corresponding column of pixels. At this point, we associate the x-coordinate of the intersection with the x-coordinate of the texture (which is determined by the value of the cell where the intersection occurred).

To apply the texture to the column, we extract a slice from the texture using the determined x-coordinate. Next, we iterate through each pixel within the slice and place them on the column, one by one.
