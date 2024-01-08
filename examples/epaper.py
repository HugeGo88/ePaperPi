from PIL import Image, ImageDraw, ImageFont
import traceback
import time
import logging
import sys
import os
import requests
from bs4 import BeautifulSoup


class word_press:
    def read_wordpress_events():
        api_url = 'https://cvjm-walheim.de/wp-json/tribe/events/v1/events?_embed&page=1'
        response = requests.get(api_url)
        response_json = response.json()
        logging.info("Events reseved")
        return response_json

    def create_images():
        edge = 10
        space = 50
        lineHeight = 27
        font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
        font22 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 22)
        logging.info("ePaper Example")
        # Clean image
        logging.info("Get data from wordpress")
        black = Image.new('RGBA', (epd.width, epd.height),
                          (255, 255, 255, 0))
        red = Image.new('RGBA', (epd.width, epd.height), (255, 255, 255, 0))
        combined = Image.new(
            'RGBA', (epd.width, epd.height), (255, 255, 255, 255))

        draw_black = ImageDraw.Draw(black)
        draw_red = ImageDraw.Draw(red)

        events = word_press.read_wordpress_events()
        line = edge
        for event in events['events']:
            soup = BeautifulSoup(event['title'], 'html.parser')
            draw_red.text((edge, line),
                          event['utc_start_date_details']['day']+"."+event['utc_start_date_details']['month'], font=font22, fill=(255, 0, 0, 255))
            line += lineHeight
            draw_black.text((edge, line),
                            soup.text, font=font22, fill=(0, 0, 0, 255))
            line += lineHeight

        combined = Image.alpha_composite(combined, black)
        combined = Image.alpha_composite(combined, red)
        return black, red, combined


class epd:
    width = 800
    height = 480


picdir = os.path.join(os.path.dirname(
    os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(
    os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)


logging.basicConfig(level=logging.DEBUG)


try:
    black, red, combined = word_press.create_images()
    black.save('images/black.png')
    red.save('images/red.png')
    combined.save('images/combined.png')
    # txt = Image.new('RGBA', (epd.width, epd.height), (255, 255, 255, 0))

    # font22 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 22)
    # d = ImageDraw.Draw(txt)

    # d.text((0, 0), "This text should be 5% alpha",
    #        fill=(255, 0, 0, 255), font=font22)
    # combined = Image.alpha_composite(red, txt)
    # combined.save('combined.png')

except IOError as e:
    logging.info(e)
