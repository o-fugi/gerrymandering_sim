import matplotlib.pyplot as plt
import numpy as np
import math as m

#Input filename
filename = "distribution.txt"

prec_dim_x = 16
prec_dim_y = 20

#Automatically creates an square array based on number of lines
#Will only work on files with perfect squares
#Might want to include a check to see if there are a perfect square number of elements(but could slow the function down)
def createarray(filename):
    #Takes all the elements from a file and creates an array with one row and x number of columns based on new lines
    arr = np.fromfile(filename, float,-1,"\r\n")
    #Finds the square root of the number of elements in the array and makes that the dimension
    #square_dimension = int(m.sqrt(len(arr)))
    #Reshapes the array based on the dimension decided
    arr = np.reshape(arr,(prec_dim_y,prec_dim_x))
    return arr

#Runs the function and inputs array into a new variable
percent_dem = createarray(filename)

#Graphs the map
plt.imshow(percent_dem, cmap='RdBu', interpolation='nearest')
plt.show()

