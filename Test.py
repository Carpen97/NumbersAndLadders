import argparse
from Game import *
from Strategy import *

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


def mutate(params, mutation_rate=0.1):
    new_params = {}
    for k, v in params.items():
        if isinstance(v, int):
            delta = random.choice([-1, 1])
        elif isinstance(v, float):
            delta = random.uniform(-0.1, 0.1)
        else:
            delta = 0
        new_params[k] = v + delta if random.random() < mutation_rate else v
    return new_params

def evaluate_strategy(individual, opponents, game_config):
    # opponents: list of other strategy dicts
    # game_config: {min, max, cubes, remove}
    players = []

    # Main individual as first player
    players.append(Player.Player("Agent", played_by_human=False,
                          strategy=individual["strategy_cls"](**individual["params"])))

    # Add opponents
    for i, op in enumerate(opponents):
        strat = op["strategy_cls"](**op["params"])
        players.append(Player.Player(f"Bot{i+1}", played_by_human=False, strategy=strat))

    game = Game.Game(players, game_config["cubes"], game_config["min"],
                game_config["max"], game_config["remove"])
    
    game.play()
    
    # Return Agent's score
    return players[0].score


def genetic_algorithm(strategy_cls, param_template, population_size=10, generations=50):
    # Try to load existing best params
    seed_params = load_best_params(strategy_cls)

    # Random initialization
    population = []

    if seed_params:
        for _ in range(int(population_size*0.5)):
            population.append({
                "strategy_cls": strategy_cls,
                "params": seed_params,
                "score": 0
            })

    # Fill the rest randomly
    while len(population) < population_size:
        random_params = {
            k: random.uniform(*v) if isinstance(v, tuple) else v
            for k, v in param_template.items()
        }
        population.append({
            "strategy_cls": strategy_cls,
            "params": random_params,
            "score": 0
        })

    for gen in range(generations):
        for individual in population:
            opponents = random.sample(population, 3)  # Simulate against others
            individual["score"] = evaluate_strategy(individual, opponents, {
                "cubes": 5, "min": 1, "max": 36, "remove": 3
            })

        population.sort(key=lambda ind: ind["score"], reverse=True)
        top_half = population[:population_size // 2]

        # Reproduce + mutate
        new_gen = []
        while len(new_gen) < population_size:
            parent = random.choice(top_half)
            child_params = mutate(parent["params"])
            new_gen.append({
                "strategy_cls": strategy_cls,
                "params": child_params,
                "score": 0
            })

        population = new_gen
        print(f"Generation {gen+1}: Best Score = {top_half[0]['score']:.2f} Params = {top_half[0]['params']}")

    return population[0]  # Best individual

best = genetic_algorithm(
    LadderBuilderStrategy,
    param_template={"gap_weight": (0, 2), "extension_gap": (0, 4), "pile_threshold": (0, 5)},
    population_size=12,
    generations=100
)

save_best_params(best)

print("Best found:", best)
