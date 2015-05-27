from PIL import Image
from PIL import ImageDraw

im = Image.new("RGB", (512, 512), "white")

draw = ImageDraw.Draw(im)
draw.line((0, 0, 512, 512), (0,0,0))
draw.line((0, 512, 512, 0), (256,0,0))
draw.point([(23,35),(123,135),(230,350)], (0,0,0))
draw.ellipse((20, 20, 25, 25), fill = 'blue', outline ='blue')
im.save("test.bmp", "BMP")

