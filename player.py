import json
import subprocess

import requests



class Player:
    VERSION = "Call me maybe"

    def betRequest(self, game_state):
        me = game_state['in_action']
        call = game_state['current_buy_in'] - game_state['players'][me]['bet']

        print self.rank_cards(me, game_state)

        print "Betting: %s" % call
        return call

    def rank_cards(self, me, game_state):
        all_cards = game_state['players'][me]['hole_cards'] + game_state['community_cards']
        raw = subprocess.check_output("curl -XGET -d 'cards=%s' http://rainman.leanpoker.org/rank" % json.dumps(all_cards), shell=True)
        data = json.loads(raw)
        return data

    def showdown(self, game_state):
        pass

    def should_raise(self, me, game_state):
        rank_data = self.rank_cards(me, game_state)
        if rank_data['rank'] >= 2:
            return True
        return False

