import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d import Axes3D
import numpy as np 

fig = plt.figure()

ax = Axes3D(fig)

# gencap is used to remove points that take too many generations (only graphs the good points)
gencap = 35
data1 = []
data2 = []
dataAvg = []
dataFinal = []


file1 = open("Test2.txt", "r")
# read all lines of file to text1
text1 = file1.read()
# map all values in file to ints
numbers1 = map(int, text1.split())
# convert to list
numbers1 = list(numbers1)
# create data points to graph in the form (Z, X, Y) (Z is vertical, X and Y are horizontal plane)
for val in range(int(len(numbers1) / 3)):
	val = val * 3
	# Population, mutation rate, generations
	point = [numbers1[val + 1], numbers1[val + 2], numbers1[val]]
	data1.append(point)
file1.close()

file2 = open("Test3.txt")
text2 = file2.read()
numbers2 = map(int, text2.split())
numbers2 = list(numbers2)
for val in range(int(len(numbers2) / 3)):
	val = val * 3
	point = [numbers2[val + 1], numbers2[val + 2], numbers2[val]]
	data2.append(point)
file2.close()

def average(data1, data2):
	# average the generations for each trial in all different tests
	array = []
	for val in range(len(data1)):
		# grab the generation values from data sets
		pnt1 = data1[val][2]
		pnt2 = data2[val][2]
		# pntAvg is the average amount of generations
		pntAvg = (pnt1 + pnt2) / 2
		# population size and mutation rate stay the same, insert average generation
		newPnt = [data1[val][0], data1[val][1], pntAvg]
		array.append(newPnt)
	return array

# dataAvg contains every data point (no generation cap)
dataAvg = average(data1, data2)

# takes points that are under gencap and adds them to new array
for point in dataAvg:
	if point[2] <= gencap:
		dataFinal.append(point)
	else:
		pass

# adds points to plot (population, mutation rate, average generation)
for point in dataFinal:
	ax.scatter(point[0], point[1], point[2])

ax.set_xlabel('population')
ax.set_ylabel('mutation rate')
ax.set_zlabel('generations')

plt.show()