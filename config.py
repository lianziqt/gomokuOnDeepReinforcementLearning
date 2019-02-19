#### SELF PLAY
EPISODES = 10
MCTS_SIMS = 30 #mcts_simulation次数
MEMORY_SIZE = 20000
TURNS_UNTIL_TAU0 = 10 # turn on which it starts playing deterministically
CPUCT = 2
EPSILON = 0.2
ALPHA = 0.8


#### RETRAINING
BATCH_SIZE = 64
EPOCHS = 1
REG_CONST = 0.0001
LEARNING_RATE = 0.1
MOMENTUM = 0.9
TRAINING_LOOPS = 5

HIDDEN_CNN_LAYERS = [
	{'filters':75, 'kernel_size': (4,4)}
	 , {'filters':75, 'kernel_size': (4,4)}
	 , {'filters':75, 'kernel_size': (4,4)}
	 , {'filters':75, 'kernel_size': (4,4)}
	 #, {'filters':75, 'kernel_size': (4,4)}
	 #, {'filters':75, 'kernel_size': (4,4)}
	]

#### EVALUATION
EVAL_EPISODES = 15
SCORING_THRESHOLD = 1.3