from PIL import Image, ImageDraw, ImageFont
import traceback
import time
import logging
import sys
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import locale

locale.setlocale(locale.LC_TIME, 'de_DE')

picdir = os.path.join(os.path.dirname(
    os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(
    os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
font22 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 22)
fontIcon = ImageFont.truetype(os.path.join(
    picdir, 'materialdesignicons-webfont.ttf'), 22)


class word_press:
    def read_wordpress_events():
        api_url = 'https://cvjm-walheim.de/wp-json/tribe/events/v1/events?_embed&page=1'
        response = requests.get(api_url)
        response_json = response.json()
        logging.info("got events")
        return response_json

    def read_wordpress_tickets():
        api_url = 'https://cvjm-walheim.de/wp-json/wp/v2/tribe_rsvp_tickets?page=1'
        response = requests.get(api_url)
        response_json = response.json()
        logging.info("got tickets")
        return response_json

    def create_images():
        edge = 10
        space = 50
        lineHeight = 27
        lineGap = 15
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
        tickets = word_press.read_wordpress_tickets()
        line = edge
        for event in events['events']:
            soup = BeautifulSoup(event['title'], 'html.parser')
            startTime = datetime.strptime(
                event['start_date'], '%Y-%m-%d %H:%M:%S')

            draw_red.text((edge + epd.width/2, line),
                          startTime.strftime('%A %d %B %Y'), font=font22, fill=(255, 0, 0, 255))
            # icon = chr(0xf207)
            # draw_red.text((edge, line),
            #               icon, font=fontIcon, fill=(255, 0, 0, 255))
            line += lineHeight
            draw_black.text((edge + epd.width/2, line),
                            soup.text, font=font22, fill=(0, 0, 0, 255))
            line += lineHeight + lineGap
        line = edge
        for ticket in tickets:

            draw_black.text((edge, line),
                            str(ticket['title']['rendered']), font=font22, fill=(0, 0, 0, 255))

            line += lineHeight
            draw_red.text((edge, line),
                          str(ticket['meta']['_stock'])+'/'+str(ticket['meta']['_tribe_ticket_capacity']), font=font22, fill=(255, 0, 0, 255))
            line += lineHeight + lineGap

        combined = Image.alpha_composite(combined, black)
        combined = Image.alpha_composite(combined, red)
        return black, red, combined


class epd:
    width = 800
    height = 480


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
