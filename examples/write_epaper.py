from PIL import Image, ImageDraw, ImageFont
import os
import logging

picdir = os.path.join(os.path.dirname(
    os.path.dirname(os.path.realpath(__file__))), 'pic')

logger = logging.getLogger(__name__)


class Epaper_screen:

    def __init__(self):
        logger.info('Create write_paper class')

        self.bottom_space = 0
        self.top_space = 0
        self.left_space = 0
        self.right_space = 0
        self.line_heigt = 10
        self.line_gap = 10

        self.width = 800
        self.height = 480

        self.combined = Image.new(
            'RGB', (self.width, self.height), (255, 255, 255))
        self.red = Image.new('1', (self.width, self.height), 255)
        self.black = Image.new('1', (self.width, self.height), 255)

        self.largeText = ImageFont.truetype(
            os.path.join(picdir, 'Font.ttc'), 22)
        self.mediumText = ImageFont.truetype(
            os.path.join(picdir, 'Font.ttc'), 16)
        self.smallText = ImageFont.truetype(
            os.path.join(picdir, 'Font.ttc'), 12)

    def write(self, text, font, color, x, y):
        if (color == 'red'):
            combined = ImageDraw.Draw(self.combined)
            combined.text((x, y),
                          text, font=font, fill=(255, 0, 0))
            red = ImageDraw.Draw(self.red)
            red.text((x, y),
                     text, font=font, fill=0)
        if (color == 'black'):
            combined = ImageDraw.Draw(self.combined)
            combined.text((x, y),
                          text, font=font, fill=(0, 0, 0))
            black = ImageDraw.Draw(self.black)
            black.text((x, y),
                       text, font=font, fill=0)

    def get_images(self):
        return self.black, self.red

    def print_images(self):
        self.combined.save('images/combined.png')
        self.red.save('images/red.png')
        self.black.save('images/black.png')
