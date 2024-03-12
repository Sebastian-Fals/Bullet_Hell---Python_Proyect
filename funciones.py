from pygame import *

def get_image(sheet, frame, width, height, scale, colour):
    img = Surface((width, height)).convert_alpha()
    img.blit(sheet, (0, 0), ((frame * width), 0, width, height))
    img = transform.scale(img, (width * scale, height * scale))
    img.set_colorkey(colour)
    return img.convert_alpha()