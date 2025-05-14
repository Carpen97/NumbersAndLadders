import json
import itertools
from Strategy import *
from Game import *
import Player
import random
import os

# === Load strategy configs ===
STRATEGY_CONFIGS = [
    {
        "name": "LadderBuilderStrategy",
        "class": LadderBuilderStrategy,
    },
    {
        "name": "RiskThresholdStrategy",
        "class": RiskThresholdStrategy,
    },
    {
        "name": "CollectorStrategy",
        "class": CollectorStrategy,
    },
    {
        "name": "ChaoticStrategy",
        "class": ChaoticStrategy,
    },
    {
        "name": "CubeConserverStrategy",
        "class": CubeConserverStrategy,
    },
]

GAME_CONFIG = {
    "cubes": 5,
    "min": 1,
    "max": 36,
    "remove": 3,
}

ROUNDS_PER_MATCH = 10
PLAYERS_PER_GAME = 4


def load_best_params(strategy_cls):
    filename = f"best_params_{strategy_cls.__name__}.json"
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Missing file: {filename}")
    with open(filename, "r") as f:
        return json.load(f)


def evaluate_strategies(strategies):
    results = {s["name"]: {"total_score": 0, "wins": 0, "games": 0} for s in strategies}

    combinations = list(itertools.combinations(strategies, PLAYERS_PER_GAME))
    for combo in combinations:
        for _ in range(ROUNDS_PER_MATCH):
            players = []
            for strat_info in combo:
                params = load_best_params(strat_info["class"])
                strat = strat_info["class"](**params)
                players.append(Player.Player(
                    name=strat_info["name"],
                    played_by_human=False,
                    strategy=strat
                ))

            game = Game(players, GAME_CONFIG["cubes"], GAME_CONFIG["min"], GAME_CONFIG["max"], GAME_CONFIG["remove"])
            game.play()

            # Rank players by score
            ranked = sorted(game.players, key=lambda p: p.score, reverse=True)
            for idx, player in enumerate(ranked):
                name = player.strategy.__class__.__name__
                results[name]["total_score"] += player.score
                results[name]["games"] += 1
                if idx == 0:
                    results[name]["wins"] += 1

    return results


def print_leaderboard(results):
    print("\n=== Evaluation Results ===")
    ranked = sorted(results.items(), key=lambda item: item[1]["total_score"] / item[1]["games"], reverse=True)
    for name, data in ranked:
        avg_score = data["total_score"] / data["games"]
        win_rate = data["wins"] / data["games"]
        print(f"{name:25} | Avg Score: {avg_score:.2f} | Win Rate: {win_rate:.2%} | Games: {data['games']}")


if __name__ == "__main__":
    results = evaluate_strategies(STRATEGY_CONFIGS)
    print_leaderboard(results)
