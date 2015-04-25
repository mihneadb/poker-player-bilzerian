import logging


logger = logging.getLogger(__name__)


class Player:
    VERSION = "Call me maybe"

    def betRequest(self, game_state):
        me = game_state['in_action']
        call = game_state['current_buy_in'] - game_state['players'][me]['bet']


        logger.info("Betting: %s" % call)
        return call

    def showdown(self, game_state):
        pass

