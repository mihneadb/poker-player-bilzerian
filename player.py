import json
import subprocess

import requests


SUM_CALL_LIMIT = 19
FACTOR_LIMIT = 1
BIG_CARDS = [10, '10', 'J', 'Q', 'K', 'A']

class Player:
    VERSION = "More sum"

    def betRequest(self, game_state):
        me = game_state['in_action']

        bet = 0

        cards = game_state['players'][me]['hole_cards']

        rank0 = cards[0]['rank']
        rank1 = cards[1]['rank']

        if ((rank0 in BIG_CARDS) and (rank1 in BIG_CARDS)) or self._is_high_pair(me, game_state):
            game_data = self.get_game_data(game_state)
            print game_data
            print "------------------------------------"
            size = len(game_state['community_cards'])
            if size == game_data['last_size'] and game_data['num_raises'] == 3:
                bet = 0
                game_data['num_raises'] = 0
                self.set_game_data(game_state, game_data)

            elif size == game_data['last_size']:
                bet = game_state['current_buy_in'] - game_state['players'][me]['bet']
                bet += game_state['minimum_raise']

                game_data['num_raises'] += 1
                self.set_game_data(game_state, game_data)

            else:
                bet = game_state['current_buy_in'] - game_state['players'][me]['bet']
                bet += game_state['minimum_raise']

                game_data['num_raises'] = 1
                game_data['last_size'] = size
                self.set_game_data(game_state, game_data)

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
            return rank0

        sum = rank0 + rank1
        if sum > SUM_CALL_LIMIT:
            return 1

        return 0

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

    def _is_high_pair(self, me, game_state):
        cards = game_state['players'][me]['hole_cards']

        rank0 = self._value_from_rank(cards[0]['rank'])
        rank1 = self._value_from_rank(cards[1]['rank'])
        if rank0 == rank1 and rank0 > 6:
            return True
        return False

    def get_game_data(self, game_state):
        name = 'game_%s' % game_state['game_id']
        try:
            f = open(name, 'r')
            data = json.load(f)
            f.close()
            return data
        except:
            return {"last_size": 0, "num_raises": 0}

    def set_game_data(self, game_state, game_data):
        name = 'game_%s' % game_state['game_id']
        try:
            f = open(name, 'w')
            json.dump(game_data, f)
            f.close()
        except:
            pass

