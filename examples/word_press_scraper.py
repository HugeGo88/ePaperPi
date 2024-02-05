import logging
import requests

logger = logging.getLogger(__name__)


class word_press_scraper:

    def __init__(self, url):
        self.url = url

    def read_wordpress_events(self):
        logger.info("Get events")
        api_url = self.url + '/wp-json/tribe/events/v1/events?_embed&page=1'
        response = requests.get(api_url)
        response_json = response.json()
        return response_json

    def read_wordpress_tickets(self):
        logger.info("Get tickets")
        api_url = self.url + '/wp-json/wp/v2/tribe_rsvp_tickets?page=1'
        response = requests.get(api_url)
        response_json = response.json()
        return response_json

    # def create_images():
    #     edge = 10
    #     space = 50
    #     lineHeight = 22
    #     lineGap = 10
    #     logging.info("ePaper Example")
    #     # Clean image
    #     logging.info("Get data from wordpress")
    #     black = Image.new('RGBA', (epd.width, epd.height),
    #                       (255, 255, 255, 0))
    #     red = Image.new('RGBA', (epd.width, epd.height), (255, 255, 255, 0))
    #     combined = Image.new(
    #         'RGBA', (epd.width, epd.height), (255, 255, 255, 255))
    #     combined_red = Image.new(
    #         'RGBA', (epd.width, epd.height), (255, 255, 255, 255))
    #     combined_black = Image.new(
    #         'RGBA', (epd.width, epd.height), (255, 255, 255, 255))

    #     draw_black = ImageDraw.Draw(black)
    #     draw_red = ImageDraw.Draw(red)

    #     events = word_press.read_wordpress_events()
    #     tickets = word_press.read_wordpress_tickets()
    #     line = edge

    #     for ticket in tickets:

    #         draw_black.text((edge + epd.width/2, line),
    #                         str(ticket['title']['rendered']), font=mediumText, fill=(0, 0, 0, 255))

    #         line += lineHeight
    #         draw_red.text((edge + epd.width/2, line),
    #                       str(ticket['meta']['_stock'])+'/'+str(ticket['meta']['_tribe_ticket_capacity'] + " übrig"), font=mediumText, fill=(255, 0, 0, 255))
    #         line += lineHeight + lineGap

    #     for event in events['events']:
    #         soup = BeautifulSoup(event['title'], 'html.parser')
    #         startTime = datetime.strptime(
    #             event['start_date'], '%Y-%m-%d %H:%M:%S')

    #         draw_black.text((edge + epd.width/2, line),
    #                         soup.text, font=mediumText, fill=(0, 0, 0, 255))

    #         draw_red.text((edge + epd.width/2 - space, line),
    #                       startTime.strftime('%d'), font=largeText, fill=(255, 0, 0, 255))

    #         line += lineHeight

    #         draw_red.text((edge + epd.width/2 - space, line),
    #                       startTime.strftime('%b'), font=largeText, fill=(255, 0, 0, 255))

    #         draw_red.text((edge + epd.width/2, line),
    #                       startTime.strftime('%H:%M')+' Uhr - '+event['venue']['venue'], font=mediumText, fill=(255, 0, 0, 255))
    #         line += lineHeight + lineGap

    #     cards = word_press.read_cards()
    #     line = edge
    #     for card in cards:
    #         duedate = ""
    #         if (card.card.duedate != None):
    #             duedate = datetime.strptime(
    #                 card.card.duedate, '%Y-%m-%dT%H:%M:%S+00:00')
    #         draw_black.text((edge, line),
    #                         str(card.card.title), font=mediumText, fill=(0, 0, 0, 255))

    #         line += lineHeight

    #         if (duedate != ''):
    #             draw_red.text((edge, line),
    #                           duedate.strftime('%d.%m') + " (" + card.stack.title + " " + card.board.title + ")", font=mediumText, fill=(255, 0, 0, 255))

    #         line += lineHeight + lineGap

    #     draw_black.text((edge, epd.height - edge - lineHeight/2),
    #                     'Letztes Update ' + datetime.now().strftime('%d.%m.%Y %H:%M'), font=smallText, fill=(0, 0, 0, 255))

    #     combined = Image.alpha_composite(combined, black)
    #     combined = Image.alpha_composite(combined, red)
    #     combined_red = Image.alpha_composite(combined_red, red)
    #     combined_black = Image.alpha_composite(combined_black, black)
    #     return combined_black, combined_red, combined
