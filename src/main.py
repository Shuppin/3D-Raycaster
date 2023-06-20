import math

from pyray      import *
from texture    import load_textures

# Initialisation -----------------------------------------------------------------------

# Render settings
renderWidth = 325
renderHeight = 240
windowScale = 4 # Each pixel is scaled up by this factor.
screenWidth = int(renderWidth*windowScale)
screenHeight = int(renderHeight*windowScale)

wallHeight = 1 # Determines how vertically 'streched' the walls will be.

floorColour = ( 130, 130, 130, 255 )
ceilColour = ( 80, 80, 80, 255 )

# 2D array of integers representing the our level.
worldMap = [
  [6,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
  [6,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [6,0,4,7,0,0,0,0,0,0,0,0,0,0,4,4,0,4,4,0,0,0,0,1],
  [6,0,6,5,0,0,0,0,0,0,0,0,0,0,4,0,0,0,4,0,0,0,0,1],
  [6,0,0,0,0,0,0,0,1,0,0,0,0,0,4,0,5,0,4,0,0,0,0,1],
  [6,0,0,0,0,0,0,0,1,0,0,0,0,0,4,0,0,0,4,0,0,0,0,1],
  [6,0,0,0,0,0,0,1,0,0,0,0,0,0,4,4,0,4,4,0,0,0,0,1],
  [6,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [6,1,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,3,0,0,0,1],
  [6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,0,0,1],
  [6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,3,0,0,0,1],
  [6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [6,0,0,0,0,0,0,0,8,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [6,0,0,0,0,0,0,0,7,0,0,0,0,0,0,0,0,0,5,0,0,0,0,1],
  [6,0,1,1,0,1,1,0,6,0,0,0,0,0,0,0,0,0,5,0,0,0,0,1],
  [6,0,0,0,0,0,0,0,5,0,0,0,0,0,0,0,0,0,5,0,0,0,0,1],
  [6,0,4,0,4,0,4,0,4,0,0,0,0,0,0,0,0,5,0,5,0,0,0,1],
  [6,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [6,0,3,3,0,3,3,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [6,0,0,0,0,0,0,0,1,0,1,0,2,0,3,0,4,0,5,0,6,0,7,1],
  [8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,1]
]

# Texture settings
textureWidth = 64
textureHeight = 64
textures = load_textures(textureWidth, textureHeight)

# Dev settings
showWallHeight = True
wallHeightOverridepx = 20
moveSpeed = 6
rotSpeed = 3

# Slow render settings
# Slow render is a feature that slows down the rendering
# process to a speed that is visible to the human eye.
slowRender = False
slowRenderSpeed = 2
totalPixelsDrawn = 0            # Represents the total number of pixels which could be drawn.
drawInstructionBuffer = []      # Holds every draw instruction and it's parameters.
renderUptoInstruction = 1       # The instruction to render up to.
instructionsPerFrame = 2        # How much to incrememnt renderUptoInstruction by each frame.

# Minimap settings
# The minimap is a top-down view of the world.
# It is made up of cells, each cell represents a single
# block in the world.
showMinimap = True
minimapBorderThicknesspx = 5
# How large (roughly) the minimap will be.
minimapTargetSize = int(screenWidth/5)
# Since we need to fit all the cells in the minimap, we need to
# make sure the dimensions of the minimap are a multiple of the number of cells.
minimapActualSize = int(minimapTargetSize/len(worldMap))*len(worldMap)
# Individual cell size components in case worldMap is not a square.
minimapCellSizeX = int(minimapTargetSize/len(worldMap[0]))
minimapCellSizeY = int(minimapTargetSize/len(worldMap))

# Camera settings
# More info in `README.md`
posX, posY = 22, 12         # player position vector
dirX, dirY = -1, 0          # camera direction vector
planeX, planeY = 0, 0.66    # camera plane vector

# Initialise the window
init_window(screenWidth, screenHeight, "3D Raycasting")
set_target_fps(60)
# --------------------------------------------------------------------------------------

def get_colour(i) -> tuple[int, int, int, int]:
    """
    Returns the RGBA value which corresponds to the integer values found in worldMap
    """
    match i:
        case 1: colour = BLUE
        case 2: colour = GREEN
        case 3: colour = GRAY
        case 4: colour = PURPLE
        case 5: colour = RED
        case 6: colour = MAROON
        case 7: colour = PINK
        case 8: colour = YELLOW
        case _: colour = BLACK
        
    return colour


while not window_should_close():

    # Reset frame independent variables
    totalPixelsDrawn = 0
    drawInstructionBuffer = []
    # TODO: Do not clear the buffer every frame, instead clear it whenever 
    # there is an update (i.e. a movement key is pressed).
    
    # Controls -----------------------------------------------------------------------------
    # Get the elapsed time of last frame drawn,
    # with a maximum of 1/60 to avoid any calculations
    # with infinity since this is what gets returned
    # on frame 0.
    dt = max(get_frame_time(), 1/60)
    
    # Scale the movement and rotation speed by the elapsed time so that
    # it feels consistent across different framerates.
    actualMoveSpeed = moveSpeed * dt
    actualRotSpeed = rotSpeed * dt
    
    # Decrease slow render mode speed
    if is_key_pressed(ord('[')):
        # Since instructionPerFrame is an integer dependant on slowRenderSpeed,
        # there is no point in allowing the multiplier to make instructionPerFrame
        # less than 1.
        if not instructionsPerFrame == 1:
            slowRenderSpeed *= 0.5
        
    # Increase slow render mode speed.
    if is_key_pressed(ord(']')):
        slowRenderSpeed *= 2
    
    # Toggle slow render mode.
    if is_key_pressed(ord('M')) and showWallHeight:
        slowRender = not slowRender
        if not slowRender:
            # If slow render was disabled, reset the renderUptoInstruction back to 0.
            renderUptoInstruction = 0

    # If slow render mode is enabled, we don't want to
    # be able to move or update the scene in anyway.
    if not slowRender:
        # Toggle wall height
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

        # Credit to cgtutor for rotation maths.

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
    # --------------------------------------------------------------------------------------

    begin_drawing() # Begin drawing to back buffer.

    # Raycasting code -----------------------------------------------------------------------

    # Not actually needed if the every pixel is re-drawn.
    #clear_background(BLACK)

    # Draw ceiling and floor
    ceilParams = (
        0,0,                                # x, y
        screenWidth,int(screenHeight/2),    # width, height
        ceilColour
    )
    floorParams = (
        0, int(screenHeight/2),             # x, y
        screenWidth, int(screenHeight/2),   # width, height
        floorColour
    )
    # If slow render mode is enabled, add to the buffer so we can draw it later.
    if slowRender:
        drawInstructionBuffer.append(("draw_rectangle", ceilParams))
        drawInstructionBuffer.append(("draw_rectangle", floorParams))
    # If slow render mode is disabled, draw it now.
    else:
        draw_rectangle(*ceilParams)
        draw_rectangle(*floorParams)

    # Array used to pass rendering data from the update loop to the draw loop.
    minimapData = []

    # Loop through every column.
    for columnIndex in range(renderWidth+1):
        # Calculate camera position, note we don't need a cameraY
        # since the raycasting is done exclusively in the x-axis.
        cameraX = 2 * columnIndex / renderWidth - 1
        # Calculate the position of the ray direction vector by offsetting the camera position.
        rayDirX = dirX + planeX * cameraX
        rayDirY = dirY + planeY * cameraX

        # Convert our position into grid (array-indexing friendly) coordinates.
        # Undefined behavoiur if posX or posY is negative,
        # or manages to be greater than the map size.
        mapX, mapY = int(posX), int(posY)

        # Since we can't divide by 0, check if the denominator is zero,
        # and if so, set it to an arbitrarily large number instead.
        deltaDistX = 1e32 if rayDirX == 0 else abs(1/rayDirX)
        deltaDistY = 1e32 if rayDirY == 0 else abs(1/rayDirY)
        
        # sideDistX represent the shortest distance along the ray direction vector
        # that intersects with the y-axis (counterintuitive I know)
        # likewise with sideDistY but with the x-axis.

        # The step vector tells us which quadrant our raycast will be stepping towards.

        # These values depend on the direction of the camera, 
        # so we have to split it into 4 conditions.
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

        # Actually peform the raycast.
        # More info on how it works in `README.md`
        while hit == 0:
            # We want to jump to the exact position of the next boundry (between two grid cells)
            # along the direction vector, either in the x or y position.
            
            # The side variable allows us to keep track of what axis (x or y) our our ray
            # hits each time, and when hit eventually becomes true,
            # the axis of the wall that we hit.
            if (sideDistX < sideDistY):
                sideDistX += deltaDistX
                mapX += stepX
                side = 0
            else:
                sideDistY += deltaDistY
                mapY += stepY
                side = 1

            # If the current square is not blank, end the loop.
            if worldMap[mapX][mapY] > 0:
                hit = 1

        # Calculate the perpendicular distance from the camera plane to the intersection.
        # Not only is this simpler than finding the true distance from the camera,
        # it also avoids the 'fisheye' effect where walls close to the center of
        # the screen appear taller than walls at the edge of the screen.
        if side == 0:
            perpendicularWallDist = sideDistX - deltaDistX
        else:
            perpendicularWallDist = sideDistY - deltaDistY

        # Calculate the exact x, y coordinates the ray intersects with.
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
        # but just in case that happens, just set the intersection
        # coordinates to the origin of the ray.
        else:
            rayIntersectionX = posX
            rayIntersectionY = posY

        # Identify the value of the cell the ray intersected with,
        # offsetting by 1 since our worldMap uses 1-8 instead of 0-7,
        # which is how our textures are stored.
        textureNum = worldMap[mapX][mapY] - 1

        # Convert intersection into local coordinates (relative to the current wall).
        if side == 0:
            wallX = rayIntersectionY - math.floor(rayIntersectionY)
        else:
            wallX = rayIntersectionX - math.floor(rayIntersectionX)

        # Map x-coordinate of wall intersection to the x-coordinate of texture file.
        textureX = textureWidth - int(wallX * textureWidth) - 1

        # If we wish to show the wall height, calculate it now.
        if showWallHeight:
            lineHeight = int(renderHeight * wallHeight / perpendicularWallDist)
        # Otherwise, use the override value (with a minimum of 1).
        else:
            lineHeight = max(int(windowScale/wallHeightOverridepx), 1)

        # Calculate the top and bottom position of the line, cropping
        # the values if they exceed the boundraries of the window.
        drawStart = int(-lineHeight / 2 + renderHeight / 2)
        if drawStart < 0:
            drawStart = 0
        drawEnd = int(lineHeight / 2 + renderHeight / 2)
        if drawEnd >= renderHeight:
            drawEnd = renderHeight

        # How much to increase the texture y-coordinate per pixel drawn onto the screen.
        step = textureHeight / lineHeight
        # Calculate intial starting coordinate
        textureY = (drawStart - (renderHeight / 2) + (lineHeight / 2)) * step
        for y in range(drawStart, drawEnd):
            
            # Extract the colour from that exact position in the texture file.
            colour = textures[textureNum][textureHeight * int(textureY) + textureX]
            
            # Increment the texture y-coordinate
            textureY += step

            # If the wall is in the y direction, halve it's colour value
            if side == 1:
                colour = (
                    int(colour[0]/2),
                    int(colour[1]/2),
                    int(colour[2]/2),
                    colour[3],
                )

            # Calculate position and size of the pixel on the screen.
            pixelParams = (
                columnIndex*windowScale, y*windowScale,
                windowScale, windowScale,
                colour
            )
            # If slow render mode is enabled, add to the buffer so we can draw it later.
            if slowRender:
                drawInstructionBuffer.append(("draw_rectangle", pixelParams))
            # If slow render mode is disabled, draw it now.
            else:
                draw_rectangle(*pixelParams)

            totalPixelsDrawn += 1
        
        # Add ray information to minimap data array
        minimapData.append((rayIntersectionX, rayIntersectionY))

    # --------------------------------------------------------------------------------------
    
    # Minimap code -------------------------------------------------------------------------
    if showMinimap:
        # The offset of the minimap
        minimapOffsetX = screenWidth-minimapTargetSize
        minimapOffsetY = screenHeight-minimapTargetSize

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

        # Draw minimap outline
        draw_rectangle(
            minimapOffsetX-minimapBorderThicknesspx,
            minimapOffsetY-minimapBorderThicknesspx,
            minimapActualSize+minimapBorderThicknesspx*2,
            minimapActualSize+minimapBorderThicknesspx*2,
            BLACK
        )

        # Draw cells onto minimap
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
        for columnIndex in range(1, len(minimapData)-1):
            data = minimapData[columnIndex]
            draw_line_ex(
                (
                    minimapOffsetX+int((data[1])*minimapCellSizeX),
                    minimapOffsetY+int(data[0]*minimapCellSizeX)
                ),
                (scaledPosX, scaledPosY),
                1.5,
                ( 255, 255, 255, 255 )
            )

        # Draw left FOV cone edge
        data = minimapData[0]
        draw_line_ex(
            (
                minimapOffsetX+int((data[1])*minimapCellSizeX),
                minimapOffsetY+int(data[0]*minimapCellSizeX)
            ),
            (scaledPosX, scaledPosY),
            3,
            ( 255, 0, 0, 255 )
        )

        # Draw right FOV cone edge
        data = minimapData[len(minimapData)-1]
        draw_line_ex(
            (
                minimapOffsetX+int((data[1])*minimapCellSizeX),
                minimapOffsetY+int(data[0]*minimapCellSizeX)
            ),
            (scaledPosX, scaledPosY),
            3,
            ( 255, 0, 0, 255 )
        )


        # Direction vector line
        draw_line_ex(
            (scaledPosX, scaledPosY),
            (scaledDirX, scaledDirY),
            1,
            RED
        )

        # Camera plane line
        draw_line_ex(
            (scaledPlaneLX, scaledPlaneLY),
            (scaledPlaneRX, scaledPlaneRY),
            1,
            BLUE
        )

        # Player circle
        draw_circle(
            scaledPosX,
            scaledPosY,
            4,
            GREEN
        )

        # Direction vector circle
        draw_circle(
            scaledDirX,
            scaledDirY,
            2,
            RED
        )

        # Right side of camera plane circle
        draw_circle(
            scaledPlaneRX,
            scaledPlaneRY,
            2,
            BLUE
        )

        # Left side of camera plane circle
        draw_circle(
            scaledPlaneLX,
            scaledPlaneLY,
            2,
            BLUE
        )
    # --------------------------------------------------------------------------------------

    if slowRender:
        
        instruction = ""
        
        # Execute each instruction in the buffer.
        for i in range(renderUptoInstruction):
            # Unpack the current instruction and parameters.
            instruction, params = drawInstructionBuffer[i]
            # Match the instruction to a function.
            match instruction:
                case "draw_rectangle":
                    draw_rectangle(*params)
                case _ as func_name:
                    print(f"WARN: Attempted to call unknown instruction: '{func_name}'")    
        
        # If the last instruction was a draw_rectangle,
        # we can safely assume that was the last pixel
        # of the most recently drawn column of pixels.
        if instruction == "draw_rectangle":
            # On this most recent column, we can draw a yellow line
            # from the top of the screen to the bottom, visualising
            # what column the ray cast is current on.
            draw_rectangle(
                params[0], 0,
                params[2], screenHeight,
                ( 253, 249, 0, 40 )
            )
            # Then we can draw a green line from the bottom middle
            # of the screen to the 2D position of that ray cast,
            # visualising the current ray cast which being perfomed.
            draw_line_ex(
                (params[0]+(windowScale/2), screenHeight/2),
                (screenWidth/2, screenHeight),
                2,
                ( 0, 228, 48, 80 )
            )

        # Calculate the number of instructions to execute per frame
        # based on the render speed, the amount of pixels visible
        # and the frame time.
        instructionsPerFrame = math.floor((totalPixelsDrawn/(10/dt))*slowRenderSpeed)
        # If this number is less than 1, we need to increase the
        # render speed until it is at least 1.
        while instructionsPerFrame < 1:
            slowRenderSpeed *= 2
            instructionsPerFrame = math.floor((totalPixelsDrawn/(10/dt))*slowRenderSpeed)
        
        # If we have not reached the end of the instruction buffer,
        # increment the instruction counter by the previously calculated
        # instructionsPerFrame.
        if renderUptoInstruction < len(drawInstructionBuffer):
            renderUptoInstruction += instructionsPerFrame
        # If we have reached the end of/gone past the end of the instruction buffer,
        # we know we have completed the visualisation of the rendering procees,
        # so we can reset all the value ready for use again.
        if renderUptoInstruction >= len(drawInstructionBuffer):
            renderUptoInstruction = 0
            slowRender = False
            drawInstructionBuffer = []
                
    # Text title ---------------------------------------------------------------------------
    draw_text(
        f"3D Raycasting | {int(1/dt)} FPS",
        20,
        20,
        20,
        WHITE
    )
    # --------------------------------------------------------------------------------------

    # Stats code ---------------------------------------------------------------------------
    # List of statistics to display on the bottom left of the screen.
    stats = [
        f"pos: ({posX:.2f}, {posY:.2f})",
        f"dir: ({dirX:.2f}, {dirY:.2f})",
        f"res: {renderHeight}x{renderWidth}",
        f"*px: {windowScale}px",
        f"spd: {'%s' % float('%.3g' % slowRenderSpeed)}x",  # Syntax for 3 significant figures
        f"#px: {renderUptoInstruction if slowRender else totalPixelsDrawn}",
    ]
    
    # Append a few extra stats specific to slow rendering.
    if slowRender:
        stats.append(f"slow: ACTIVE")
        stats.append(f"iinc: {instructionsPerFrame} pixels/frame")

    # Draw each stat to the screen, offsetting each line vertically by 20 pixels.
    for i, stat in enumerate(stats[::-1]):
        draw_text(
            stat,
            20,
            screenHeight-((i+2)*20),
            20,
            WHITE
        )
    # --------------------------------------------------------------------------------------

    end_drawing()  # Swap buffers

close_window()