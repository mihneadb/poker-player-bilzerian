
class Player:
    VERSION = "Default Python folding player"

    def betRequest(self, game_state):
        me = game_state['in_action']
        call = game_state['current_buy_in'] - game_state['players'][me]['bet']
        return call

    def showdown(self, game_state):
        pass

