from credentials import credentials
from deck.api import NextCloudDeckAPI
from deck.models import Board, Card, Stack
from requests.auth import HTTPBasicAuth
import logging

logger = logging.getLogger(__name__)

nc = NextCloudDeckAPI(
    "https://nextcloud.cvjm-walheim.de:443", HTTPBasicAuth(credentials.user, credentials.password), ssl_verify=True
)


class Task:
    def __init__(self, card, stack, board):
        self.card = card
        self.stack = stack
        self.board = board

    def __str__(self):
        return f'Board {self.board.title}'

    card = Card
    stack = Stack
    board = Board


def read_cards():
    all_tasks: Task = []
    boards = nc.get_boards()

    for board in boards:
        logging.info(board.title)
        stacks = nc.get_stacks(board.id)
        for stack in stacks:
            if (stack.title == "Erledigt"):
                continue
            logging.info(stack.title)
            for card in stack.cards:
                logging.debug(Task(card=card, stack=stack, board=board))
                all_tasks.append(Task(card=card, stack=stack, board=board))
                logging.info(card.title)
    return all_tasks


if __name__ == '__main__':
    read_cards()
