import json
import subprocess

import requests


SUM_CALL_LIMIT = 19
FACTOR_LIMIT = 1

class Player:
    VERSION = "More sum"

    def betRequest(self, game_state):
        me = game_state['in_action']

        bet = 0
        if (not game_state['community_cards']) and self._should_call(me, game_state):
            bet = game_state['current_buy_in'] - game_state['players'][me]['bet']

            if bet > (game_state['players'][me]['stack'] / 2.0):
                return 0

        elif game_state['community_cards']:
            factor = self.should_raise(me, game_state)
            bet = (game_state['current_buy_in'] -
                   game_state['players'][me]['bet'])

            if (factor < 2) and (bet > (game_state['players'][me]['stack'] / 2.0)):
                return 0

            if factor > FACTOR_LIMIT:
                bet += game_state['minimum_raise']
                bet += factor * (game_state['minimum_raise'] / 5)

            if factor is 0 and len(game_state['community_cards']) == 3:
                bet = 0

            if factor <= FACTOR_LIMIT and len(game_state['community_cards']) > 3:
                bet = 0

        bet = int(bet)

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

    def should_raise(self, me, game_state):
        rank_data = self.rank_cards(me, game_state)
        if rank_data == "":
            return 0
        if rank_data['rank'] >= 2:
            return rank_data['rank']
        return 0

    def _should_call(self, me, game_state):
        cards = game_state['players'][me]['hole_cards']

        rank0 = self._value_from_rank(cards[0]['rank'])
        rank1 = self._value_from_rank(cards[1]['rank'])
        if rank0 == rank1:
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
