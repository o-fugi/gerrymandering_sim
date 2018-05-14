import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon
import math as m

filename = 'distribution.txt'
district_dim = 4

def assigndistricts(y_point, x_point):
    x_count = 1
    y_count = 1
    x_lapsed = False
    y_lapsed = False
    for y in range(0, prec_dim):
	x_count = 1
	x_lapsed = False
	if (y_point + prec_dim/district_dim * (y_count-1) <= y and not y_lapsed):
	    y_count += 1
	if (y_count > district_dim):
	    y_count = 1
	    y_lapsed = True
	for x in range(0, prec_dim):
	    if (x_point + prec_dim/district_dim * (x_count-1) <= x and not x_lapsed):
                x_count += 1
	    if (x_count > district_dim):
                x_count = 1
                x_lapsed = True
	    district_num = x_count + y_count*(prec_dim/district_dim - 1) - 1
            data[district_num][assigndistricts.percent] += arr[x][y]/((prec_dim/district_dim) ** 2)
    assigndistricts.percent += 1

#you want a 2d array, each row is a distribution (one for each districting!) for one district.

#Takes all the elements from a file and creates an array with one row and x number of columns based on new lines
arr = np.fromfile(filename, float,-1,"\r\n")
#Finds the square root of the number of elements in the array and makes that the dimension
prec_dim = int(m.sqrt(len(arr)))
#Reshapes the array based on the dimension decided
arr = np.reshape(arr,(prec_dim,prec_dim))

assigndistricts.percent = 0
data = np.zeros((district_dim**2, (prec_dim/district_dim)**2))
for y in range(0, int(prec_dim/district_dim)):
    for x in range(0, int(prec_dim/district_dim)):
        assigndistricts(y, x)

fig, ax = plt.subplots()
ax.boxplot(data)

plt.show()
