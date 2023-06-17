from os     import listdir
from PIL    import Image
from PIL    import UnidentifiedImageError

# TODO: Add a more robust texture system, the current system works,
# but it relies to much on the fact that the texture directory only contains textures.
def load_textures(textureWidth, textureHeight, dir='img/') -> list[tuple[int, int, int, int]]:
    """
    Loads all image files within a given directory
    into an array of RGBA tuples.
    """
    # In case any images fail to load, the texture will
    # just be a blank black texture as a fall back
    textures = [[(0,0,0,255)]*textureHeight*textureWidth]*len(listdir(dir))

    # dir needs to end with a slash, so *hopefully*
    # this should catch any minor errors
    if not dir.endswith('/'):
        dir += '/'

    # Iterate through each file within the direction
    for i, filename in enumerate(listdir(dir)):
        try:
            # Attempt to load the file as an image
            img = Image.open(dir+filename)
        except UnidentifiedImageError:
            # File type is not supported by pillow
            continue
        except FileNotFoundError:
            # File is removed in the time since listdir() and now
            continue
        except Exception as err_msg:
            # Covers any edge cases, a texture failing to load shouldn't be fatal.
            print(f"Error reading file '{filename}' - {err_msg}")

        img = img.resize((textureWidth, textureHeight))  # Resize the image to 64x64

        pixels = img.load()  # Get pixel data

        pixelList = []

        for y in range(textureHeight):
            for x in range(textureWidth):
                pixelList.append(pixels[x, y])  # Append pixel information to list

        textures[i] = pixelList  # Add the list of pixels to the set of textures

    return textures