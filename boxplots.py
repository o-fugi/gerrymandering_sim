import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon
import math as m
import sys
import random

#constants
filename = 'distribution.txt'
prec_dim_x = 100
prec_dim_y = 100
district_dim_x = 4 #there are 4x4 districts
district_dim_y = 4 #there are 4x4 districts
num_cities = 4
dist_factor = .8
most_democratic = .6
percent_decrease = .96

#TODO:  population density in urban areas
# non-rectangular states
# how fast can it get?
# ** research on percent_decrease, num_cities, dist_factor, most_democratic **
# regression

def wrap(diff, wrap_value):
    if diff < 0:
        diff = diff+wrap_value
    return float(diff)

def norm(diff, identifier):
    if(identifier == 'x'):
        diff = prec_dim_x - m.fabs(diff) if m.fabs(diff)>prec_dim_x/2 else diff
    elif(identifier == 'y'):
        diff = prec_dim_y - m.fabs(diff) if m.fabs(diff)>prec_dim_y/2 else diff
    else:
        print("in function norm, axis must be x or y")
    return diff

def giveDistrict(acount, districting):

    district_x = districting % (prec_dim_x / district_dim_x) #x-offset (how far from 0, 0 is district 1)
    district_y = m.floor(districting / (prec_dim_x/district_dim_x)) #y-offset
    
    x_dim = m.floor(wrap(acount%prec_dim_x - district_x, prec_dim_x) / prec_dim_x * district_dim_x)
    y_dim = m.floor(wrap(m.floor(acount/prec_dim_x) - district_y, prec_dim_y) / prec_dim_y * district_dim_y)

    district = int(x_dim) + int(y_dim*(district_dim_x))
    return district #value from 0 to district_dim**2 - 1

def distFromCity(y, x, city_locations):
    distance = 1000000000000
    for city in city_locations:
	distance = min(distance, m.sqrt(m.pow(norm(x - city[0], 'x'), 2) + m.pow(norm(y-city[1], 'y'), 2)))
    distance = m.pow(distance, dist_factor)
    return distance
    
if __name__ == '__main__':
    if(len(sys.argv) > 1):
        show = True
    else:
        show = False

    #generate the maps
    print("generating the maps")
    city_locations = np.empty([num_cities, 2])
    for city in city_locations:
	city[0] = random.randint(0, prec_dim_x - 1)
        city[1] = random.randint(0, prec_dim_y - 1)

    percent_dem = np.empty([prec_dim_y, prec_dim_x])
    for y, row in enumerate(percent_dem):
        for x, column in enumerate(row):
            factor = distFromCity(y, x, city_locations)
            row[x] = most_democratic * m.pow(percent_decrease, factor)

    #Takes all the elements from a file and creates an array with one row and x number of columns based on new lines
    arr = np.fromfile(filename, float,-1,"\r\n")
    #Finds the square root of the number of elements in the array and makes that the dimension
    #prec_dim = int(m.sqrt(len(arr)))
    #Reshapes the array based on the dimension decided
    #arr = np.reshape(arr,(prec_dim_y,prec_dim_x))
    #print(arr)
    if(0):
        percent_dem = arr

    districting_averages = np.zeros([prec_dim_x/district_dim_x*prec_dim_y/district_dim_y, district_dim_x*district_dim_y])  #one row for each districting, 16 districts in a districting

    #proof of giveDistrict effectiveness
    if (show):
        show_districts = np.zeros([prec_dim_x*prec_dim_y, 1])

    medians = np.zeros([district_dim_x*district_dim_y])

    print("assigning districting values")
    #assign districting values
    #there's a better way to do this
    #for d, districting in enumerate(districting_averages): #for each possible districting...
    #    print("on districting %d" % d)
    #    for index, value in enumerate(np.nditer(percent_dem)): #add on the percent_dem for each district
    #        district = giveDistrict(index, d)
    #        if(show):
    #            show_districts[index] = float(district) / 8
    #        districting[district] += value
    #    if (show):
    #        plt.imshow(np.reshape(show_districts, (prec_dim_y, prec_dim_x)), cmap='RdBu', interpolation='nearest')
    #        plt.show()

    #or...
    by_district_arr = np.zeros([district_dim_x*district_dim_y, prec_dim_x/district_dim_x*prec_dim_y/district_dim_y])
    for num, district in enumerate(by_district_arr): 
        print("district_num = %d" % num)
        for d, districting in enumerate(district):
            x1 = int(d % (prec_dim_x/district_dim_x) + (num%district_dim_x)*(prec_dim_x/district_dim_x))
            x2 = int(x1 + prec_dim_x/district_dim_x)
            y1 = int(m.floor(d / (prec_dim_x/district_dim_x)) + m.floor(num/district_dim_y)*prec_dim_y/district_dim_y)
            y2 = int(y1 + prec_dim_y/district_dim_y)
            #print("%d, %d, %d, %d" % (x1, x2, y1, y2))
            district[d] = np.mean(np.take(np.take(percent_dem, range(y1, y2), axis=0, mode='wrap'), range(x1, x2), axis=1, mode='wrap'))

    districting_averages = np.divide(districting_averages, prec_dim_x/district_dim_x*prec_dim_y/district_dim_y)

    print(by_district_arr)

    #to sort them, you have to transpose the array, sort, then transpose back
    print("transposing and sorting the array")
    #rows_are_districts = np.transpose(districting_averages)
    rows_are_districts = by_district_arr
    for index, district in enumerate(rows_are_districts):
        medians[index] = np.median(district)

    print("assigning medians")
    meaninds = medians.argsort()
    rows_are_districts = rows_are_districts[meaninds]
    #districting_averages = np.transpose(rows_are_districts)
    by_district_arr = rows_are_districts

    print("making the plots")
    fig, ax = plt.subplots()
    #ax.boxplot(districting_averages)
    ax.boxplot(np.transpose(by_district_arr))

    fig, ax1 = plt.subplots()

    plt.imshow(percent_dem, cmap='RdBu', interpolation='nearest')
    plt.show()
