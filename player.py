import json
import subprocess

import requests


SUM_CALL_LIMIT = 16

class Player:
    VERSION = "Bet me maybe"

    def betRequest(self, game_state):
        me = game_state['in_action']

        print self.rank_cards(me, game_state)

        bet = 0
        if self._should_call(me, game_state):
            bet = game_state['current_buy_in'] - game_state['players'][me]['bet']

        print "Betting: %s" % bet
        return bet

    def rank_cards(self, me, game_state):
        data = ""
        try:
            all_cards = game_state['players'][me]['hole_cards'] + game_state['community_cards']
            raw = subprocess.check_output("curl -XGET -d 'cards=%s' http://rainman.leanpoker.org/rank" % json.dumps(all_cards), shell=True)
            data = json.loads(raw)
        except:
            data = ""
        return data

    def showdown(self, game_state):
        pass

    def _should_call(self, me, game_state):
        cards = game_state['players'][me]['hole_cards']

        rank0 = self._value_from_rank(cards[0]['rank'])
        rank1 = self._value_from_rank(cards[1]['rank'])
        if rank0 == rank1:
            return True
        if cards[0]['suit'] == cards[1]['suit']:
            return True
        if abs(rank0 - rank1) == 1:
            return True

        sum = rank0 + rank1
        return sum > SUM_CALL_LIMIT

    def _value_from_rank(self, rank):
        if rank == 'J':
            return 12
        if rank == 'Q':
            return 13
        if rank == 'K':
            return 14
        if rank == 'A':
            return 15

        return int(rank)
