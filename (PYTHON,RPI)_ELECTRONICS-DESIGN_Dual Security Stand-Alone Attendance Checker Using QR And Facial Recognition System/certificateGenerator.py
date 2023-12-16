from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

msg1 = "MAPÚA UNIVERSITY"
msg2 = "Certificate of Completion"
msg3 = "PAMBID, LUIS DANIEL A."
msg4 = "March 19, 2019"
msg5 = "TIME IN: 11:59 PM"
msg6 = "TIME OUT: 12:00 PM"
msg7 = "DURATION: 03:00:00 MINUTES"


def doText(draw, font, size, msg, width, height):
    selectFont = ImageFont.truetype(font, size=size)
    w, h = draw.textsize(msg, font=selectFont)
    draw.text(((width - w) / 2, height), msg, (39, 37, 37), font=selectFont)


img = Image.open("certTemplate.png")
draw = ImageDraw.Draw(img)
width, height = img.size
doText(draw, "Nunito-Light.ttf", 80, msg1, width, 20)
doText(draw, "vivaldi.ttf", 60, msg2, width, 150)
doText(draw, "cambria.ttf", 60, msg3, width, 250)
doText(draw, "vivaldi.ttf", 60, msg4, width, 350)
doText(draw, "cambria.ttf", 40, msg5, width, 450)
doText(draw, "cambria.ttf", 40, msg6, width, 500)
doText(draw, "cambria.ttf", 40, msg7, width, 550)
img.save("CERTIFICATE_TEST.png", "PNG", resolution=100.0)
