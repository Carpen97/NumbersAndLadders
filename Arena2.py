from Strategy import *
from Game import *
import Player
import random
import json
import matplotlib.pyplot as plt

# Import your GA methods here
from Arena import genetic_algorithm, save_best_params  # Replace with actual module

# Strategies and param spaces to train
STRATEGY_TRAINING_CONFIGS = [
	{
		"name": "LadderBuilderStrategy",
		"class": LadderBuilderStrategy,
		"param_template": {
			"gap_weight": (0, 2),
			"extension_gap": (0, 4),
			"pile_threshold": (0, 5),
		}
	},
	{
		"name": "RiskThresholdStrategy",
		"class": RiskThresholdStrategy,
		"param_template": {
			"risk_multiplier": (0.01, 0.2),
		}
	},
	{
		"name": "CollectorStrategy",
		"class": CollectorStrategy,
		"param_template": {
			"cutoff": (10, 30),
		}
	},
	{
		"name": "ChaoticStrategy",
		"class": ChaoticStrategy,
		"param_template": {
			"yolo_chance": (0.0, 0.5),
			"pay_chance": (0.0, 1.0),
		}
	},
	{
		"name": "CubeConserverStrategy",
		"class": CubeConserverStrategy,
		"param_template": {
			"low_cube_threshold": (1, 5),
			"pile_threshold": (0, 4),
		}
	},
]

# Evaluation config
GAME_CONFIG = {
	"cubes": 5,
	"min": 1,
	"max": 36,
	"remove": 3,
}

# General GA config
POPULATION_SIZE = 10
GENERATIONS = 50
SEED = 42

def run_training():
	for config in STRATEGY_TRAINING_CONFIGS:
		print(f"\n=== Training {config['name']} ===")

		best, param_history, score_history = genetic_algorithm(
			config["class"],
			param_template=config["param_template"],
			population_size=POPULATION_SIZE,
			generations=GENERATIONS,
			seed=SEED
		)

		save_best_params(best)

		# Plot results
		plt.figure(figsize=(10, 4))
		for param, values in param_history.items():
			plt.plot(values, label=param)
		plt.title(f"{config['name']} - Parameter Evolution")
		plt.xlabel("Generation")
		plt.ylabel("Value")
		plt.legend()
		plt.grid(True)
		plt.tight_layout()
		plt.show()

		# Plot score history
		plt.figure(figsize=(10, 3))
		plt.plot(score_history, label="Best Score", color="black")
		plt.title(f"{config['name']} - Score Over Generations")
		plt.xlabel("Generation")
		plt.ylabel("Score")
		plt.grid(True)
		plt.tight_layout()
		plt.show()

		print("Final best:", best)

if __name__ == "__main__":
	run_training()
