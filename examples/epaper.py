from bs4 import BeautifulSoup
from datetime import datetime
from deck.api import NextCloudDeckAPI
from deck.models import Board, Card, Stack
from PIL import Image, ImageDraw, ImageFont
from requests.auth import HTTPBasicAuth
import locale
import logging
import os
import requests
import sys
from credentials import credentials

locale.setlocale(locale.LC_TIME, 'de_DE')

picdir = os.path.join(os.path.dirname(
    os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(
    os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

font26 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 26)
font22 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 22)
font12 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 12)
fontIcon = ImageFont.truetype(os.path.join(
    picdir, 'materialdesignicons-webfont.ttf'), 22)


nc = NextCloudDeckAPI(
    "https://nextcloud.cvjm-walheim.de:443", HTTPBasicAuth(credentials.user, credentials.password), ssl_verify=True
)


class word_press:
    def read_cards():
        all_cards = []
        boards = nc.get_boards()

        for board in boards:
            print(board.title)
            stacks = nc.get_stacks(board.id)
            for stack in stacks:
                if (stack.title != "Offen"):
                    continue
                print(stack.title)
                for card in stack.cards:
                    all_cards.append(card)
                    print(card.title)
        return all_cards

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

        for ticket in tickets:

            draw_black.text((edge + epd.width/2, line),
                            str(ticket['title']['rendered']), font=font22, fill=(0, 0, 0, 255))

            line += lineHeight
            draw_red.text((edge + epd.width/2, line),
                          str(ticket['meta']['_stock'])+'/'+str(ticket['meta']['_tribe_ticket_capacity']), font=font22, fill=(255, 0, 0, 255))
            line += lineHeight + lineGap

        for event in events['events']:
            soup = BeautifulSoup(event['title'], 'html.parser')
            startTime = datetime.strptime(
                event['start_date'], '%Y-%m-%d %H:%M:%S')
            # icon = chr(0xf207)
            # draw_red.text((edge, line),
            #               icon, font=fontIcon, fill=(255, 0, 0, 255))
            draw_black.text((edge + epd.width/2, line),
                            soup.text, font=font22, fill=(0, 0, 0, 255))

            draw_red.text((edge + epd.width/2 - space, line),
                          startTime.strftime('%d'), font=font26, fill=(255, 0, 0, 255))

            line += lineHeight

            draw_red.text((edge + epd.width/2 - space, line),
                          startTime.strftime('%b'), font=font26, fill=(255, 0, 0, 255))

            draw_red.text((edge + epd.width/2, line),
                          startTime.strftime('%H:%M')+' Uhr - '+event['venue']['venue'], font=font22, fill=(255, 0, 0, 255))
            line += lineHeight + lineGap

        cards = word_press.read_cards()
        line = edge
        for card in cards:
            duedate = ""
            if (card.duedate != None):
                duedate = datetime.strptime(
                    card.duedate, '%Y-%m-%dT%H:%M:%S+00:00')
            draw_black.text((edge, line),
                            str(card.title), font=font22, fill=(0, 0, 0, 255))

            line += lineHeight

            if (duedate != ''):
                draw_red.text((edge, line),
                              duedate.strftime('%d.%m'), font=font22, fill=(255, 0, 0, 255))

            line += lineHeight + lineGap

        draw_black.text((edge, epd.height - edge - lineHeight/2),
                        'Letztes Update ' + datetime.now().strftime('%d.%m.%Y %H:%M'), font=font12, fill=(0, 0, 0, 255))

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
