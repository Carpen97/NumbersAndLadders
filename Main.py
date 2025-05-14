import argparse
from Game import * 
from Strategy import *
def parse_args():
    parser = argparse.ArgumentParser(
        description="Play Numbers & Ladders",
        formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, max_help_position=35, width=100)
    )

    parser.add_argument("--players", type=int, default=4, help="Total number of players.")
    parser.add_argument(
        "--humans", nargs='*', default=[],
        help="List of names (e.g., --humans Alice Bob Charlie)"
    )
    parser.add_argument("--cubes", type=int, default=5, help="Starting cubes per player (default=5).")
    parser.add_argument("--min", type=int, default=1, help="Lowest number (default = 1).")
    parser.add_argument("--max", type=int, default=36, help="Highest number (default = 35).")
    parser.add_argument("--remove", type=int, default=3, help="How many numbers to remove from the stack (default = 3).")
    parser.add_argument("-silent", action="store_true", help="Run a silent simulation of the game without terminal output")
    return parser.parse_args()

import json
import os

def get_strategy_filename(strategy_cls):
    return f"best_params_{strategy_cls.__name__}.json"

def save_best_params(individual):
    filename = get_strategy_filename(individual["strategy_cls"])
    with open(filename, "w") as f:
        json.dump(individual["params"], f, indent=2)
    print(f"Saved best parameters to {filename}")

def load_best_params(strategy_cls):
    filename = get_strategy_filename(strategy_cls)
    if not os.path.exists(filename):
        print(f"No saved parameters found for {strategy_cls.__name__}")
        return None
    with open(filename, "r") as f:
        params = json.load(f)
    print(f"Loaded saved parameters from {filename}")
    return params

if __name__ == "__main__":
    args = parse_args()

    players = []
    human_names = set(args.humans)
    total_players = max(len(human_names), args.players)  # or another logic you prefer

    for i in range(total_players):
        name = f"Player {i+1}"
        if i < len(args.humans):
            name = args.humans[i]
        is_human = name in human_names

        strategy = random.choice([
            LadderBuilderStrategy(**(load_best_params(LadderBuilderStrategy))),
            LadderBuilderStrategy(**(load_best_params(LadderBuilderStrategy))),
            LadderBuilderStrategy(**(load_best_params(LadderBuilderStrategy))),
        ])
        players.append(Player.Player(name, played_by_human=is_human, strategy=strategy))

    game = Game.Game(players, args.cubes, args.min, args.max, args.remove)
    game.play(in_terminal= not args.silent)

