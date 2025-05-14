import Game
import Player
import random

class Strategy:
    def __init__(self, **params):
        self.params = params

    @property
    def name(self):
        return self.__class__.__name__

    def make_choice(self, game: Game, player: Player):
        raise NotImplementedError

class Simlple(Strategy):
    def make_choice(s, game: Game, player: Player):
        num = game.num

        #Always take numbers adjacent to current numbers
        for n in player.numbers:
            if num == n+1 or num == n-1:
                return "t"

        threshold_to_take = 0.03 * game.pile
        p = random.uniform(0,1)
        if threshold_to_take > p: return "t"
        else: return "p"
    
class LadderBuilderStrategy(Strategy):
    def make_choice(self, game: Game, player: Player):
        num = game.num
        gap = self.params.get("gap_weight", 1)
        extension_gap = self.params.get("extension_gap", 2)
        pile_threshold = self.params.get("pile_threshold", 1)

        for n in player.numbers:
            if abs(n - num) <= gap:
                return "t"
        if game.pile > pile_threshold and any(abs(num - n) <= extension_gap for n in player.numbers):
            return "t"
        return "p"


class CollectorStrategy(Strategy):
    def make_choice(self, game: Game, player: Player):
        num = game.num
        cutoff = self.params.get("cutoff", (game.lowest_number + game.highest_number) // 2)
        if num < cutoff:
            return "t"
        return "p"

class ChaoticStrategy(Strategy):
    def make_choice(self, game: Game, player: Player):
        r = random.random()
        yolo = self.params.get("yolo_chance", 0.1)
        pay = self.params.get("pay_chance", 0.5)

        if r < yolo:
            return "t"
        elif r < pay:
            return "p"
        return "t"

class RiskThresholdStrategy(Strategy):
    def make_choice(self, game: Game, player: Player):
        num = game.num
        for n in player.numbers:
            if abs(n - num) == 1:
                return "t"

        risk_multiplier = self.params.get("risk_multiplier", 0.03)
        threshold_to_take = risk_multiplier * game.pile
        if random.uniform(0, 1) < threshold_to_take:
            return "t"
        return "p"

