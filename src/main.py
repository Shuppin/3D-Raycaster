import math
from pyray import *

# Initialisation -----------------------------------------------------------------------
screenWidth = 1300
screenHeight = 960

moveSpeed = 6
rotSpeed = 3

wallHeight = 2

floorColour = ( 130, 130, 130, 255 )
ceilColour = ( 80, 80, 80, 255 )

worldMap = [
  [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
  [1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,5,5,0,0,0,0,0,0,0,0,0,0,4,4,0,4,4,0,0,0,0,1],
  [1,0,5,5,0,0,0,0,0,0,0,0,0,0,4,0,0,0,4,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,1,0,0,0,0,0,4,0,5,0,4,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,1,0,0,0,0,0,4,0,0,0,4,0,0,0,0,1],
  [1,0,0,0,0,0,0,1,0,0,0,0,0,0,4,4,0,4,4,0,0,0,0,1],
  [1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,1,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,3,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,3,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,5,0,0,0,0,1],
  [1,0,1,1,0,1,1,0,2,0,0,0,0,0,0,0,0,0,5,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,5,0,0,0,0,1],
  [1,0,4,0,4,0,4,0,4,0,0,0,0,0,0,0,0,5,0,5,0,0,0,1],
  [1,0,0,0,0,0,0,0,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,3,3,0,3,3,0,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,1,0,1,0,2,0,3,0,4,0,5,0,6,0,5,1],
  [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
];

# Dev settings
showWallHeight = True
wallHeightOverridepx = 20
minimapSize = 300

minimapCellSizeX = int(minimapSize/len(worldMap[0]))
minimapCellSizeY = int(minimapSize/len(worldMap))

# Camera settings
posX, posY = 22, 12  # x and y position of the player
dirX, dirY = -1, 0  # camera direction vector
planeX, planeY = 0, 0.66  # camera plane vector

# Initialise the window
init_window(screenWidth, screenHeight, "3D Raycasting")
set_target_fps(60)
# --------------------------------------------------------------------------------------

def get_colour(i):
    match i:
        case 1: colour = RED
        case 2: colour = GREEN
        case 3: colour = BLUE
        case 4: colour = PURPLE
        case 5: colour = YELLOW
        case _: colour = BLACK
        
    return colour


while not window_should_close():
    
    # Update -------------------------------------------------------------------------------
    dt = get_frame_time()
    actualMoveSpeed = moveSpeed * dt
    actualRotSpeed = rotSpeed * dt

    if is_key_pressed(ord('X')):
        showWallHeight = not showWallHeight

    # Forward
    if is_key_down(ord('W')):
        if worldMap[int(posX + dirX * actualMoveSpeed)][int(posY)] == False:
            posX += dirX * actualMoveSpeed
        if worldMap[int(posX)][int(posY + dirY * actualMoveSpeed)] == False:
            posY += dirY * actualMoveSpeed

    # Backwards
    if is_key_down(ord('S')):
        if worldMap[int(posX - dirX * actualMoveSpeed)][int(posY)] == False:
            posX -= dirX * actualMoveSpeed
        if worldMap[int(posX)][int(posY - dirY * actualMoveSpeed)] == False:
            posY -= dirY * actualMoveSpeed

    # Credit to cgtutor for rotation maths

    # Rotate left
    if is_key_down(ord('A')):
        oldDirX = dirX
        dirX = dirX * math.cos(actualRotSpeed) - dirY * math.sin(actualRotSpeed)
        dirY = oldDirX * math.sin(actualRotSpeed) + dirY * math.cos(actualRotSpeed)
        oldPlaneX = planeX
        planeX = planeX * math.cos(actualRotSpeed) - planeY * math.sin(actualRotSpeed)
        planeY = oldPlaneX * math.sin(actualRotSpeed) + planeY * math.cos(actualRotSpeed)

    # Rotate right
    if is_key_down(ord('D')):
        oldDirX = dirX
        dirX = dirX * math.cos(-actualRotSpeed) - dirY * math.sin(-actualRotSpeed)
        dirY = oldDirX * math.sin(-actualRotSpeed) + dirY * math.cos(-actualRotSpeed)
        oldPlaneX = planeX
        planeX = planeX * math.cos(-actualRotSpeed) - planeY * math.sin(-actualRotSpeed)
        planeY = oldPlaneX * math.sin(-actualRotSpeed) + planeY * math.cos(-actualRotSpeed)

    # Array used to pass rendering data from the update loop to the draw loop
    columnData = []

    # Loop through every column
    for columnIndex in range(screenWidth):
        # Calculate camera position, note we don't need a cameraY
        cameraX = 2 * columnIndex / screenWidth - 1
        # Calculate the position of the ray direction vector by offsetting the camera position
        rayDirX = dirX + planeX * cameraX
        rayDirY = dirY + planeY * cameraX

        # Convert our position into grid coordinates
        mapX, mapY = int(posX), int(posY)

        # Since we can't divide by 0, check if the denominator is zero,
        # and if so, set it to an arbitrarily large number instead
        deltaDistX = 1e32 if rayDirX == 0 else abs(1/rayDirX)
        deltaDistY = 1e32 if rayDirY == 0 else abs(1/rayDirY)
        
        # sideDistX represent the shortest distance along the ray direction vector
        # that intersects with the y-axis (counterintuitive I know)
        # likewise with sideDistY but with the x-axis

        # The step vector tells us which direction we are stepping in

        # These values depend on the direction of the camera, so we have to split it into 4 conditions
        if rayDirX < 0:
            stepX = -1
            sideDistX = (posX - mapX) * deltaDistX
        else:
            stepX = 1
            sideDistX = (mapX + 1 - posX) * deltaDistX

        if rayDirY < 0:
            stepY = -1
            sideDistY = (posY - mapY) * deltaDistY
        else:
            stepY = 1
            sideDistY = (mapY + 1 - posY) * deltaDistY

        hit = 0

        # Perform DDA Raycast
        while hit == 0:

            # Jump to the exact position of the next boundry along the direction vector, either in the x or y position
            # The side variable allows us to keep track of what axis our our ray 7
            # hits each time, ultimately being the axis of the wall that we hit.
            # This is later used to shade the wall a darker colour
            if (sideDistX < sideDistY):
                sideDistX += deltaDistX
                mapX += stepX
                side = 0
            else:
                sideDistY += deltaDistY
                mapY += stepY
                side = 1

            # If the current square is not blank, end the loop
            if worldMap[mapX][mapY] > 0:
                hit = 1

        # Calculate the perpendicular distance from the camera plane to the intersection
        # Not only is this simpler than finding the true distance from the camera, it also avoids the 'fisheye' effect
        if side == 0:
            perpendicularWallDist = sideDistX - deltaDistX
        else:
            perpendicularWallDist = sideDistY - deltaDistY

        # Calculate the exact x, y coordinates the ray intersects with
        if side == 0 and stepX == -1:
            rayIntersectionX = mapX+1
            rayIntersectionY = posY + perpendicularWallDist * rayDirY
        elif side == 0 and stepX == 1:
            rayIntersectionX = mapX
            rayIntersectionY = posY + perpendicularWallDist * rayDirY

        elif side == 1 and stepY == -1:
            rayIntersectionX = posX + perpendicularWallDist * rayDirX
            rayIntersectionY = mapY+1
        elif side == 1 and stepY == 1:
            rayIntersectionX = posX + perpendicularWallDist * rayDirX
            rayIntersectionY = mapY
        # It shouldn't be possible for all of the above to return false,
        # but just in case that happens, just set the intersection coordinates to the origin of the ray
        else:
            rayIntersectionX = posX
            rayIntersectionY = posY

        if showWallHeight:
            # Calculate the height of the line we need to draw
            lineHeight = int(screenHeight * wallHeight / perpendicularWallDist)
        else:
            lineHeight = wallHeightOverridepx

        # Calculate the top and bottom position of the line, truncating
        # the values if they exceed the boundraries of the window
        drawStart = int(-lineHeight / 2 + screenHeight / 2)
        if drawStart < 0:
            drawStart = 0
        drawEnd = int(lineHeight / 2 + screenHeight / 2)
        if drawEnd >= screenHeight:
            drawEnd = screenHeight-1

        # Calculate which colour to draw the line
        colour = get_colour(worldMap[mapX][mapY])

        # If the wall is in the y direction, halve it's colour value
        if side == 1:
            colour = (
                int(colour[0]/2),
                int(colour[1]/2),
                int(colour[2]/2),
                colour[3],
            )

        # Add ray information to array
        columnData.append((drawStart, drawEnd, rayIntersectionX, rayIntersectionY, colour))

    # The offset of the minimap
    minimapOffsetX = screenWidth-minimapSize
    minimapOffsetY = screenHeight-minimapSize

    # The position of the player position transformed onto the minimap
    scaledPosX = minimapOffsetX+int(posY*minimapCellSizeX)
    scaledPosY = minimapOffsetY+int(posX*minimapCellSizeY)

    # Represents how large the small camera diagram should be
    cameraVisualisationScale = 3

    # The position of the direction vector transformed onto the minimap
    scaledDirX = scaledPosX+int(dirY*cameraVisualisationScale*minimapCellSizeX)
    scaledDirY = scaledPosY+int(dirX*cameraVisualisationScale*minimapCellSizeY)

    # The position of the right corner of the camera plane transformed onto the minimap
    scaledPlaneRX = scaledDirX+int(planeY*cameraVisualisationScale*minimapCellSizeX)
    scaledPlaneRY = scaledDirY+int(planeX*cameraVisualisationScale*minimapCellSizeY)

    # The position of the left corner of the camera plane transformed onto the minimap
    scaledPlaneLX = scaledDirX-int(planeY*cameraVisualisationScale*minimapCellSizeX)
    scaledPlaneLY = scaledDirY-int(planeX*cameraVisualisationScale*minimapCellSizeY)
    # --------------------------------------------------------------------------------------
    
    # Draw ---------------------------------------------------------------------------------
    begin_drawing()

    clear_background(BLACK)

    # Draw ceiling
    draw_rectangle(
        0,0,
        screenWidth, int(screenHeight/2),
        ceilColour
    )

    # Draw floor
    draw_rectangle(
        0, int(screenHeight/2),
        screenWidth, int(screenHeight/2),
        floorColour
    )
    
    # Draw each pixel column
    for columnIndex in range(len(columnData)):
        data = columnData[columnIndex]
        draw_line_ex(
            (columnIndex, data[0]),
            (columnIndex, data[1]),
            1,
            data[4]
        )

    # Minimap code

    # Draw level onto minimap
    for row in range(len(worldMap)):
        for cell in range(len(worldMap[row])):
            draw_rectangle(
                minimapOffsetX+(cell*minimapCellSizeX),
                minimapOffsetY+(row*minimapCellSizeY),
                minimapCellSizeX,
                minimapCellSizeY,
                get_colour(worldMap[row][cell])
            )

    # Draw FOV cone
    for columnIndex in range(1, len(columnData)-1):
        data = columnData[columnIndex]
        draw_line_ex(
            (
                minimapOffsetX+int((data[3])*minimapCellSizeX),
                minimapOffsetY+int(data[2]*minimapCellSizeX)
            ),
            (scaledPosX, scaledPosY),
            1.5,
            ( 255, 255, 255, 255 )
        )

    # draw left FOV cone edge
    data = columnData[0]
    draw_line_ex(
        (
            minimapOffsetX+int((data[3])*minimapCellSizeX),
            minimapOffsetY+int(data[2]*minimapCellSizeX)
        ),
        (scaledPosX, scaledPosY),
        3,
        ( 255, 0, 0, 255 )
    )

    # draw right FOV cone edge
    data = columnData[len(columnData)-1]
    draw_line_ex(
        (
            minimapOffsetX+int((data[3])*minimapCellSizeX),
            minimapOffsetY+int(data[2]*minimapCellSizeX)
        ),
        (scaledPosX, scaledPosY),
        3,
        ( 255, 0, 0, 255 )
    )


    # direction vector line
    draw_line_ex(
        (scaledPosX, scaledPosY),
        (scaledDirX, scaledDirY),
        1,
        RED
    )

    # camera plane line
    draw_line_ex(
        (scaledPlaneLX, scaledPlaneLY),
        (scaledPlaneRX, scaledPlaneRY),
        1,
        BLUE
    )

    # player circle
    draw_circle(
        scaledPosX,
        scaledPosY,
        4,
        GREEN
    )

    # direction vector circle
    draw_circle(
        scaledDirX,
        scaledDirY,
        2,
        RED
    )

    # right side of camera plane circle
    draw_circle(
        scaledPlaneRX,
        scaledPlaneRY,
        2,
        BLUE
    )

    # left side of camera plane circle
    draw_circle(
        scaledPlaneLX,
        scaledPlaneLY,
        2,
        BLUE
    )

    # Text overlay
    draw_text(
        f"3D Raycasting | {int(1/dt) if dt > 0 else 'inf'} FPS",
        20,
        20,
        20,
        WHITE
    )

    end_drawing()
    # --------------------------------------------------------------------------------------

close_window()