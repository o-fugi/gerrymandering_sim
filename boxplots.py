import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon
import math as m
import sys

filename = 'distribution.txt'
prec_dim_x = 16
prec_dim_y = 20
district_dim_x = 4 #there are 4x4 districts
district_dim_y = 5 #there are 4x4 districts

def norm(diff, norm_value):
    if diff < 0:
        diff = diff+norm_value
    return float(diff)

def giveDistrict(acount, districting):

    district_x = districting % (prec_dim_x / district_dim_x) #x-offset (how far from 0, 0 is district 1)
    district_y = m.floor(districting / (prec_dim_x/district_dim_x)) #y-offset
    
    x_dim = m.floor(norm(acount%prec_dim_x - district_x, prec_dim_x) / prec_dim_x * district_dim_x)
    y_dim = m.floor(norm(m.floor(acount/prec_dim_x) - district_y, prec_dim_y) / prec_dim_y * district_dim_y)
    if (y_dim < 0):
        print("%d, %d, %d, %d, %d" % (acount, prec_dim_x, district_y, prec_dim_y, district_dim_y))

    district = int(x_dim) + int(y_dim*(district_dim_x))
    return district #value from 0 to district_dim**2 - 1
    
if __name__ == '__main__':
    if(len(sys.argv) > 1):
        show = True
    else:
        show = False

    #Takes all the elements from a file and creates an array with one row and x number of columns based on new lines
    arr = np.fromfile(filename, float,-1,"\r\n")
    #Finds the square root of the number of elements in the array and makes that the dimension
    #prec_dim = int(m.sqrt(len(arr)))
    #Reshapes the array based on the dimension decided
    arr = np.reshape(arr,(prec_dim_y,prec_dim_x))

    districting_averages = np.zeros([prec_dim_x/district_dim_x*prec_dim_y/district_dim_y, district_dim_x*district_dim_y])  #one row for each districting, 16 districts in a districting

    #proof of giveDistrict effectiveness
    if (show):
        show_districts = np.zeros([prec_dim_x*prec_dim_y, 1])

    medians = np.zeros([district_dim_x*district_dim_y])

    #assign districting values
    for d, districting in enumerate(districting_averages): #for each possible districting...
        for index, value in enumerate(np.nditer(arr)): #add on the percent_dem for each district
            if(value == 0):
                print("value is 0")
            district = giveDistrict(index, d)
            if(show):
                show_districts[index] = float(district) / 8
            districting[district] += value
            """if(m.isnan(districting[district])):
                print("nan, districting: %d, index: %d, value: %d, district: %d" % (d, index, value, district))"""
        if (show):
            plt.imshow(np.reshape(show_districts, (prec_dim_y, prec_dim_x)), cmap='RdBu', interpolation='nearest')
            plt.show()

    districting_averages = np.divide(districting_averages, prec_dim_x/district_dim_x*prec_dim_y/district_dim_y)

    print(districting_averages)

    #to sort them, you have to transpose the array, sort, then transpose back
    print("transposing and sorting the array")
    rows_are_districts = np.transpose(districting_averages)
    for index, district in enumerate(rows_are_districts):
        medians[index] = np.median(district)

    print("assigning medians")
    meaninds = medians.argsort()
    rows_are_districts = rows_are_districts[meaninds]
    districting_averages = np.transpose(rows_are_districts)

    print("making the plots")
    fig, ax = plt.subplots()
    ax.boxplot(districting_averages)

    fig, ax1 = plt.subplots()
    percent_dem = arr

    plt.imshow(percent_dem, cmap='RdBu', interpolation='nearest')
    plt.show()
