import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon
import math as m

filename = 'distribution.txt'
district_dim = 12 #there are 4x4 districts

def norm(diff, norm_value):
    if diff < 0:
        diff = diff+norm_value
    return float(diff)

def giveDistrict(acount, districting):

    district_x = districting % district_dim #type of x-districting
    district_y = m.floor(districting / district_dim) #type of y-districting
    
    x_dim = m.floor(norm((acount%prec_dim) - district_x, prec_dim) / prec_dim * district_dim)
    y_dim = m.floor(norm(m.floor(acount/prec_dim) - district_y, prec_dim) / prec_dim * district_dim)
    
    district = x_dim + y_dim*(prec_dim/district_dim) -1
    return int(district) #value from 0 to district_dim**2 - 1
    
if __name__ == '__main__':
    #Takes all the elements from a file and creates an array with one row and x number of columns based on new lines
    arr = np.fromfile(filename, float,-1,"\r\n")
    #Finds the square root of the number of elements in the array and makes that the dimension
    prec_dim = int(m.sqrt(len(arr)))
    #Reshapes the array based on the dimension decided
    arr = np.reshape(arr,(prec_dim,prec_dim))

    districting_averages = np.empty([(prec_dim/district_dim)**2, district_dim**2])  #one row for each districting, 16 districts in a row

    #proof of giveDistrict effectiveness
    #show_districts = np.empty([prec_dim**2, 1])

    medians = np.empty([(prec_dim/district_dim)**2])

    #assign districting values
    for d, districting in enumerate(districting_averages):
        for index, value in enumerate(np.nditer(arr)):
            #show_districts[index] = float(giveDistrict(index, d)) / 8
            districting[giveDistrict(index, d)] += value
        #plt.imshow(np.reshape(show_districts, (prec_dim, prec_dim)), cmap='RdBu', interpolation='nearest')
        #plt.show()

    #to sort them, you have to transpose the array, sort, then transpose back
    rows_are_districts = np.transpose(districting_averages)
    for index, district in enumerate(rows_are_districts):
        medians[index] = np.median(district)

    meaninds = medians.argsort()
    rows_are_districts = rows_are_districts[meaninds]
    districting_averages = np.transpose(rows_are_districts)

    fig, ax = plt.subplots()
    districting_averages = np.divide(districting_averages, (prec_dim/district_dim)**2)
    ax.boxplot(districting_averages)

    fig, ax1 = plt.subplots()
    percent_dem = arr

    plt.imshow(percent_dem, cmap='RdBu', interpolation='nearest')
    plt.show()
