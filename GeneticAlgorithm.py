import pygame as pg
import random
import math

pg.init()

# window dimensions
display_width = 800
display_height = 600

# color defs
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 100)
white = (255, 255, 255)

gameDisplay = pg.display.set_mode((display_width, display_height))
clock = pg.time.Clock()


# returns array of for moves, each index is a move for a frame. 0=up, 1=down, 2=left, 3=right
def init_agents(num_agents):
	agent_moves = []
	for i in range(num_agents):
		moves = []
		for i in range(50):
			direction = random.randrange(0, 4)
			if direction == 0:
				moves.append(direction)
			if direction == 1:
				moves.append(direction)
			if direction == 2:
				moves.append(direction)
			if direction == 3:
				moves.append(direction)
		agent_moves.append(moves)
	return agent_moves

# ranks the agents on their x, y distance from the red square (in terms of pixels, not moves) using pythagorean theorem
def fitness(agents_pos):
	agents_fitness = []
	for pos in agents_pos:
		x_distance = redbox_x - pos[0]
		y_distance = redbox_y - pos[1]
		angle_distance = math.sqrt((x_distance ** 2) + (y_distance ** 2))
		fitness = angle_distance / (math.sqrt((redbox_x ** 2) + (redbox_y ** 2 )))
		agents_fitness.append(fitness)
	agents_pos = []
	return agents_fitness

# finds average fitness of all agents in population
def average_fitness(agents_fitness):
	total = sum(agents_fitness)
	average = total / len(agents_fitness)
	best_fitness = min(agents_fitness)
	print('average fitness: ', average, 'best fitness: ', best_fitness)
	return average, best_fitness

# if fitness = 0, runs game_loop with only the agent w/ fitness = 0
def zero_fitness(new_population, agents_fitness):
	zero_fitness_index = agents_fitness.index(0)
	end = False
	while not end:
		game_loop(new_population)
		for event in pg.event.get():
			if event.type == pg.QUIT:
				end = True
				quit()

# adds the best fitness agents to best (adds their index)
def top_percentage(agents_fitness):
	best = []
	agents_fitness_scrap = []
	top = len(agents_fitness) * .05
	top = int(top)
	for item in agents_fitness:
		agents_fitness_scrap.append(item)
	for i in range(top):
		lowest = min(agents_fitness_scrap)
		lowest_index = agents_fitness_scrap.index(lowest)
		best.append(lowest_index)
		del agents_fitness_scrap[lowest_index]
	return best

# breeds agents based on best, takes first "half" of one and the second "half"
# of the other, adds them (in order) to the offspring. Repeats until 
# the population is equal to what it started
def crossover(best, new_population):

	new_population___ = []
	offspring = []
	for index in best:
		new_population___.append(new_population[index])

	while (len(new_population___) < num_agents):
		first_parent = random.randrange(0, (len(best) - 1))
		second_parent = random.randrange(0, (len(best) - 1))
		if second_parent == first_parent:
			second_parent = random.randrange(0, (len(best) - 1))
		parent_one = best[first_parent]
		parent_two = best[second_parent]
		

		splice_point = random.randrange(1, (len(new_population[0]) - 1))

		first_half = []
		second_half = []
		for i in range(splice_point):
			first_half.append(new_population[parent_one][i])
		for i in range(len(new_population[0]) - splice_point):
			x = i + splice_point
			second_half.append(new_population[second_parent][x])
		offspring = []
		offspring.extend(first_half)
		offspring.extend(second_half)
	

		new_population___.append(offspring)
		offspring = []
	return new_population___

# based on random chance, decides a random position inside of
# the DNA to mutate/change into a new move/number
def mutation(new_population):
	for agent in range(len(new_population)):
		chance = random.randrange(0, 101)
		if chance <= mutate_rate:
			change_point = random.randrange(0, len(new_population[agent]))
			direction = random.randrange(0, 4)
			if direction == 0:
				new_population[agent][change_point] = 0
			if direction == 1:
				new_population[agent][change_point] = 1
			if direction == 2:
				new_population[agent][change_point] = 2
			if direction == 3:
				new_population[agent][change_point] = 3
		else:
			pass
	return new_population

def game_loop(new_population):
	gameExit = False
	
	frame = 0
	agents_pos = []
	pg.draw.rect(gameDisplay, blue, (100, 100, 10, 10))
	for i in range(num_agents):
		pos = [player_start_x, player_start_y]
		agents_pos.append(pos)

	while not gameExit:

		for event in pg.event.get():
			if event.type == pg.QUIT:
				gameExit = True
				quit()


		gameDisplay.fill(pg.Color("black"))

		pg.draw.rect(gameDisplay, red, (redbox_x, redbox_y, 5, 5))

		# 0=up, 1=down, 2=left, 3=right
		# pos = [ [x, y], [x, y], [x, y] ]
		for i in range(len(new_population)):
			if new_population[i][frame] == 0:
				agents_pos[i][1] = agents_pos[i][1] - 10
			elif new_population[i][frame] == 1:
				agents_pos[i][1] = agents_pos[i][1] + 10
			elif new_population[i][frame] == 2:
				agents_pos[i][0] = agents_pos[i][0] - 10
			elif new_population[i][frame] == 3:
				agents_pos[i][0] = agents_pos[i][0] + 10

		for i in range(len(new_population)):
			pg.draw.rect(gameDisplay, blue, (agents_pos[i][0], agents_pos[i][1], 10, 10))
		
		frame = frame + 1
		if frame == len(new_population[0]):
			return agents_pos
			gameExit = True

		pg.display.update()
		clock.tick(frame_rate)

# hyperparameters

agents_fitness = []

redbox_x = 100
redbox_y = 300
player_start_x = 100
player_start_y = 100
frame_rate = 100
num_agents = 500
# mutation rate as a percent. EX "3" would take the top 3 percent
mutate_rate = 3


def gen_alg(number_agents, mutation_rate):
	num_agents = number_agents
	mutate_rate = mutation_rate
	proceed = True
	new_population = init_agents(num_agents)
	generations = 0
	while proceed:
		generations = generations + 1
		agents_pos = game_loop(new_population)
		agents_fitness = fitness(agents_pos)
		best = top_percentage(agents_fitness)
		average, best_fitness = average_fitness(agents_fitness)

		if min(agents_fitness) == 0:
			proceed = False
		if generations >= max_generations:
			generations = -1
			proceed = False
		else:
			new_population = crossover(best, new_population)
			new_population = mutation(new_population)


	return generations

max_agents = 100
max_mutate = 50
max_generations = 2000

f = open("Test4_11-2-18.txt", "x")

for num_agents in range(6, max_agents):
	num_agents = num_agents * 10
	for mutate_rate in range(max_mutate):
		generations = gen_alg(num_agents, mutate_rate)
		if generations == -1:
			f = open("Test3_11-2-18.txt", "a")
			f.write("N/A" + " " + str(num_agents) + " " + str(mutate_rate) + '\n')
		else:
			f = open("Test3_11-2-18.txt", "a")
			f.write(str(generations) + " " + str(num_agents) + " " + str(mutate_rate) +'\n')




#gen_alg(500, 3)

pg.quit()
quit()