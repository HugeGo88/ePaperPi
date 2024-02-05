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
from write_epaper import Epaper_screen
from word_press_scraper import word_press_scraper

locale.setlocale(locale.LC_TIME, 'de_DE')

picdir = os.path.join(os.path.dirname(
    os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(
    os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

largeText = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 22)
mediumText = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 16)
smallText = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 12)
fontIcon = ImageFont.truetype(os.path.join(
    picdir, 'materialdesignicons-webfont.ttf'), 22)


# nc = NextCloudDeckAPI(
#     "https://nextcloud.cvjm-walheim.de:443", HTTPBasicAuth(credentials.user, credentials.password), ssl_verify=True
# )


# class Task:
#     def __init__(self, card, stack, board):
#         self.card = card
#         self.stack = stack
#         self.board = board

#     card = Card
#     stack = Stack
#     board = Board


# class word_press:
#     def read_cards():
#         all_tasks = []
#         boards = nc.get_boards()

#         for board in boards:
#             logging.info(board.title)
#             stacks = nc.get_stacks(board.id)
#             for stack in stacks:
#                 if (stack.title == "Erledigt"):
#                     continue
#                 logging.info(stack.title)
#                 for card in stack.cards:
#                     all_tasks.append(Task(card=card, stack=stack, board=board))
#                     logging.info(card.title)
#         return all_tasks

#     def read_wordpress_events():
#         api_url = 'https://cvjm-walheim.de/wp-json/tribe/events/v1/events?_embed&page=1'
#         response = requests.get(api_url)
#         response_json = response.json()
#         logging.info("got events")
#         return response_json

#     def read_wordpress_tickets():
#         api_url = 'https://cvjm-walheim.de/wp-json/wp/v2/tribe_rsvp_tickets?page=1'
#         response = requests.get(api_url)
#         response_json = response.json()
#         logging.info("got tickets")
#         return response_json

#     def create_images():
#         edge = 10
#         space = 50
#         lineHeight = 22
#         lineGap = 10
#         logging.info("ePaper Example")
#         # Clean image
#         logging.info("Get data from wordpress")
#         black = Image.new('RGBA', (epd.width, epd.height),
#                           (255, 255, 255, 0))
#         red = Image.new('RGBA', (epd.width, epd.height), (255, 255, 255, 0))
#         combined = Image.new(
#             'RGBA', (epd.width, epd.height), (255, 255, 255, 255))
#         combined_red = Image.new(
#             'RGBA', (epd.width, epd.height), (255, 255, 255, 255))
#         combined_black = Image.new(
#             'RGBA', (epd.width, epd.height), (255, 255, 255, 255))

#         draw_black = ImageDraw.Draw(black)
#         draw_red = ImageDraw.Draw(red)

#         events = word_press.read_wordpress_events()
#         tickets = word_press.read_wordpress_tickets()
#         line = edge

#         for ticket in tickets:

#             draw_black.text((edge + epd.width/2, line),
#                             str(ticket['title']['rendered']), font=mediumText, fill=(0, 0, 0, 255))

#             line += lineHeight
#             draw_red.text((edge + epd.width/2, line),
#                           str(ticket['meta']['_stock'])+'/'+str(ticket['meta']['_tribe_ticket_capacity'] + " übrig"), font=mediumText, fill=(255, 0, 0, 255))
#             line += lineHeight + lineGap

#         for event in events['events']:
#             soup = BeautifulSoup(event['title'], 'html.parser')
#             startTime = datetime.strptime(
#                 event['start_date'], '%Y-%m-%d %H:%M:%S')

#             draw_black.text((edge + epd.width/2, line),
#                             soup.text, font=mediumText, fill=(0, 0, 0, 255))

#             draw_red.text((edge + epd.width/2 - space, line),
#                           startTime.strftime('%d'), font=largeText, fill=(255, 0, 0, 255))

#             line += lineHeight

#             draw_red.text((edge + epd.width/2 - space, line),
#                           startTime.strftime('%b'), font=largeText, fill=(255, 0, 0, 255))

#             draw_red.text((edge + epd.width/2, line),
#                           startTime.strftime('%H:%M')+' Uhr - '+event['venue']['venue'], font=mediumText, fill=(255, 0, 0, 255))
#             line += lineHeight + lineGap

#         cards = word_press.read_cards()
#         line = edge
#         for card in cards:
#             duedate = ""
#             if (card.card.duedate != None):
#                 duedate = datetime.strptime(
#                     card.card.duedate, '%Y-%m-%dT%H:%M:%S+00:00')
#             draw_black.text((edge, line),
#                             str(card.card.title), font=mediumText, fill=(0, 0, 0, 255))

#             line += lineHeight

#             if (duedate != ''):
#                 draw_red.text((edge, line),
#                               duedate.strftime('%d.%m') + " (" + card.stack.title + " " + card.board.title + ")", font=mediumText, fill=(255, 0, 0, 255))

#             line += lineHeight + lineGap

#         draw_black.text((edge, epd.height - edge - lineHeight/2),
#                         'Letztes Update ' + datetime.now().strftime('%d.%m.%Y %H:%M'), font=smallText, fill=(0, 0, 0, 255))

#         combined = Image.alpha_composite(combined, black)
#         combined = Image.alpha_composite(combined, red)
#         combined_red = Image.alpha_composite(combined_red, red)
#         combined_black = Image.alpha_composite(combined_black, black)
#         return combined_black, combined_red, combined


# class epd:
#     width = 800
#     height = 480


def print_events(epaper):
    wp = word_press_scraper(url='https://cvjm-walheim.de')
    events = wp.read_wordpress_events()
    y = 0
    for event in events['events']:
        title = BeautifulSoup(event['title'], 'html.parser')
        logging.info(title.text)
        epaper.write(text=title.text, font=largeText,
                     x=420, y=y, color='black')
        y += epaper.line_heigt
        epaper.write(text=title.text, font=largeText,
                     x=420, y=y, color='red')
        y += epaper.line_heigt
        y += epaper.line_gap


logging.basicConfig(level=logging.DEBUG)


try:
    # black, red, combined = word_press.create_images()
    # black.save('images/black.png')
    # red.save('images/red.png')
    # combined.save('images/combined.png')

    epaper = Epaper_screen()

    print_events(epaper)

    # epaper.write(text='Test', font=largeText, x=10, y=10, color='red')
    # epaper.write(text='Test', font=mediumText, x=200, y=10, color='black')
    epaper.print_images()


except IOError as e:
    logging.error(e)
