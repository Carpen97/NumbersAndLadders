import argparse
from Game import *
from Strategy import *

import json
import os
import random
import matplotlib.pyplot as plt


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

def mutate(params, mutation_rate=0.1, clamp_ranges=None):
	new_params = {}
	for k, v in params.items():
		if isinstance(v, int):
			delta = random.choice([-1, 1])
		elif isinstance(v, float):
			delta = random.uniform(-0.2, 0.2)
		else:
			delta = 0
		new_val = v + delta if random.random() < mutation_rate else v
		if clamp_ranges and k in clamp_ranges:
			min_val, max_val = clamp_ranges[k]
			new_val = max(min_val, min(new_val, max_val))
		new_params[k] = new_val
	return new_params

def evaluate_strategy(individual, opponents, game_config):
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
	return players[0].score  # Return Agent's score

def genetic_algorithm(strategy_cls, param_template, population_size=10, generations=100, seed=None):
	if seed is not None:
		random.seed(seed)

	seed_params = load_best_params(strategy_cls)
	population = []

	if seed_params:
		for _ in range(int(population_size * 0.5)):
			population.append({
				"strategy_cls": strategy_cls,
				"params": seed_params,
				"score": 0
			})

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

	param_history = {key: [] for key in param_template}
	score_history = []

	for gen in range(generations):
		for individual in population:
			opponents = random.sample(population, 3)
			individual["score"] = evaluate_strategy(individual, opponents, {
				"cubes": 5, "min": 1, "max": 36, "remove": 3
			})

		population.sort(key=lambda ind: ind["score"], reverse=True)
		top_half = population[:population_size // 2]

		# Track best parameters and score
		best_params = top_half[0]["params"]
		for key in param_template:
			param_history[key].append(best_params[key])
		score_history.append(top_half[0]["score"])

		# Reproduce + mutate
		new_gen = []
		while len(new_gen) < population_size:
			parent = random.choice(top_half)
			child_params = mutate(parent["params"], mutation_rate=0.3, clamp_ranges=param_template)
			new_gen.append({
				"strategy_cls": strategy_cls,
				"params": child_params,
				"score": 0
			})

		population = new_gen
		print(f"Generation {gen+1}: Best Score = {top_half[0]['score']:.2f} Params = {top_half[0]['params']}")

	return population[0], param_history, score_history


# === Run the genetic algorithm ===
best, param_history, score_history = genetic_algorithm(
	LadderBuilderStrategy,
	param_template={
		"gap_weight": (0, 2),
		"extension_gap": (0, 4),
		"pile_threshold": (0, 5)
	},
	population_size=12,
	generations=1000,
	seed=42  # Optional: set for reproducibility
)

save_best_params(best)

# === Plot parameter evolution ===
plt.figure(figsize=(10, 6))
for param, values in param_history.items():
	plt.plot(values, label=param)

plt.xlabel("Generation")
plt.ylabel("Parameter Value")
plt.title("Evolution of Parameters Over Generations")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# === Plot score evolution ===
plt.figure(figsize=(10, 4))
plt.plot(score_history, label="Best Score", color="black")
plt.xlabel("Generation")
plt.ylabel("Score")
plt.title("Best Agent Score Over Generations")
plt.grid(True)
plt.tight_layout()
plt.show()

print("Best found:", best)
