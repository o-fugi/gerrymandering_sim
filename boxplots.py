import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon
import math as m
import sys
import random

#constants
filename = 'distribution.txt'
prec_dim_x = 16
prec_dim_y = 20
district_dim_x = 4 #there are 4x4 districts
district_dim_y = 4 #there are 4x4 districts
num_cities = 4
dist_factor = .7
most_democratic = .6
percent_decrease = .96
weighted = False

percent_dem = np.zeros([prec_dim_y, prec_dim_x])
population = np.zeros([prec_dim_y, prec_dim_x])

#TODO:  population density in urban areas
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

def showDistricts():
    districting_averages = np.zeros([prec_dim_x/district_dim_x*prec_dim_y/district_dim_y, district_dim_x*district_dim_y])  #one row for each districting, 16 districts in a districting

    print("assigning districting values")
    show_districts = np.zeros([prec_dim_x*prec_dim_y, 1])
    for d, districting in enumerate(districting_averages): #for each possible districting...
        for index, value in enumerate(np.nditer(percent_dem)): #add on the percent_dem for each district
            district = giveDistrict(index, d)
            show_districts[index] = float(district) / 8
        plt.imshow(np.reshape(show_districts, (prec_dim_y, prec_dim_x)), cmap='RdBu', interpolation='nearest')
        plt.show()

def readFromFile():
    #Takes all the elements from a file and creates an array with one row and x number of columns based on new lines
    arr = np.fromfile(filename, float,-1,"\r\n")
    #Finds the square root of the number of elements in the array and makes that the dimension
    #prec_dim = int(m.sqrt(len(arr)))
    #Reshapes the array based on the dimension decided
    arr = np.reshape(arr,(prec_dim_y,prec_dim_x))
    percent_dem = arr

def makeCityDistribution():
    print("generating the maps")
    city_locations = np.empty([num_cities, 2])
    for city in city_locations:
        city[0] = random.randint(0, prec_dim_x - 1)
        city[1] = random.randint(0, prec_dim_y - 1)
    
    # to keep city locations constant between runs, uncomment and change num_cities = 2
    # city_locations[0][0] = 2
    # city_locations[0][1] = 2
    # city_locations[1][0] = 9
    # city_locations[1][1] = 9

    for y, row in enumerate(percent_dem):
        for x, column in enumerate(row):
            factor = distFromCity(y, x, city_locations)
            row[x] = most_democratic * m.pow(percent_decrease, factor)
            if factor < prec_dim_x*.1:
                population[y][x] = 3000
            else:
                population[y][x] = 1000

    return percent_dem

def randomWithoutReplacement(arr):
    arr = np.reshape(arr, arr.size)
    np.random.shuffle(arr)
    arr = np.reshape(arr, (prec_dim_y, prec_dim_x))

    return arr

def randomWithReplacement(arr):
    copy = np.reshape(arr, arr.size)
    for row in arr:
        for element in row:
            element = np.random.choice(copy)

    return arr

def assignDistricts(percent_dem):
    by_district_arr = np.zeros([int(district_dim_x*district_dim_y), int(prec_dim_x/district_dim_x*prec_dim_y/district_dim_y)])
    for num, district in enumerate(by_district_arr): 
        for d, districting in enumerate(district):
            x1 = int(d % (prec_dim_x/district_dim_x) + (num%district_dim_x)*(prec_dim_x/district_dim_x))
            x2 = int(x1 + prec_dim_x/district_dim_x)
            y1 = int(m.floor(d / (prec_dim_x/district_dim_x)) + m.floor(num/district_dim_y)*prec_dim_y/district_dim_y)
            y2 = int(y1 + prec_dim_y/district_dim_y)
            dist_box = np.take(np.take(percent_dem, range(y1, y2), axis=0, mode='wrap'), range(x1, x2), axis=1, mode='wrap')
            population_box =  np.take(np.take(population, range(y1, y2), axis=0, mode='wrap'), range(x1, x2), axis=1, mode='wrap')
            if (weighted):
                district[d] = np.average(dist_box, weights=population_box)
            else:
                district[d] = np.average(dist_box)
    return by_district_arr

def makePlots(by_district_arr):
    by_district_arr = np.sort(by_district_arr, axis=0)
    print("making the plots")
    fig, ax = plt.subplots()
    ax.boxplot(np.transpose(by_district_arr))

    ax.set_xlabel("district")
    ax.set_ylabel("percent Democratic")

    fig, ax1 = plt.subplots()
    plt.imshow(percent_dem, cmap='RdBu', interpolation='nearest')
    plt.show()

if __name__ == '__main__':
    if(len(sys.argv) > 1):
        showDistricts()

    percent_dem = makeCityDistribution()
    percent_dem_copy = percent_dem
    by_district_arr = assignDistricts(percent_dem)

    #makePlots(by_district_arr)
    by_district_arr = np.sort(by_district_arr, axis=0)
    print("making the plots")
    fig, ax = plt.subplots()
    ax.boxplot(np.transpose(by_district_arr))

    ax.set_title("Organized into Cities")
    ax.set_xlabel("district")
    ax.set_ylabel("percent Democratic")

    #fig, ax1 = plt.subplots()
    #plt.imshow(percent_dem, cmap='RdBu', interpolation='nearest')

    percent_dem = randomWithoutReplacement(percent_dem)
    by_district_arr = assignDistricts(percent_dem)

    #makePlots(by_district_arr)
    by_district_arr = np.sort(by_district_arr, axis=0)
    print("making the plots")
    fig, ax1 = plt.subplots()
    ax1.boxplot(np.transpose(by_district_arr))

    ax1.set_title("Random Without Replacement")
    ax1.set_xlabel("district")
    ax1.set_ylabel("percent Democratic")

    #fig, ax1 = plt.subplots()
    #plt.imshow(percent_dem, cmap='RdBu', interpolation='nearest')

    percent_dem = randomWithReplacement(percent_dem)
    by_district_arr = assignDistricts(percent_dem)

    #makePlots(by_district_arr)
    by_district_arr = np.sort(by_district_arr, axis=0)
    print("making the plots")
    fig, ax2 = plt.subplots()
    ax2.boxplot(np.transpose(by_district_arr))

    ax2.set_title("Random With Replacement")
    ax2.set_xlabel("district")
    ax2.set_ylabel("percent Democratic")

    #fig, ax1 = plt.subplots()
    #plt.imshow(percent_dem, cmap='RdBu', interpolation='nearest')
    plt.show()

    weighted = True

    by_district_arr = assignDistricts(percent_dem_copy)

    #makePlots(by_district_arr)
    by_district_arr = np.sort(by_district_arr, axis=0)
    print("making the plots")
    fig, ax = plt.subplots()
    ax.boxplot(np.transpose(by_district_arr))

    ax.set_title("Organized into Cities")
    ax.set_xlabel("district")
    ax.set_ylabel("percent Democratic")

    #fig, ax1 = plt.subplots()
    #plt.imshow(percent_dem, cmap='RdBu', interpolation='nearest')

    percent_dem_copy = randomWithoutReplacement(percent_dem_copy)
    by_district_arr = assignDistricts(percent_dem_copy)

    #makePlots(by_district_arr)
    by_district_arr = np.sort(by_district_arr, axis=0)
    print("making the plots")
    fig, ax1 = plt.subplots()
    ax1.boxplot(np.transpose(by_district_arr))

    ax1.set_title("Random Without Replacement")
    ax1.set_xlabel("district")
    ax1.set_ylabel("percent Democratic")

    #fig, ax1 = plt.subplots()
    #plt.imshow(percent_dem, cmap='RdBu', interpolation='nearest')

    percent_dem_copy = randomWithReplacement(percent_dem_copy)
    by_district_arr = assignDistricts(percent_dem_copy)

    #makePlots(by_district_arr)
    by_district_arr = np.sort(by_district_arr, axis=0)
    print("making the plots")
    fig, ax2 = plt.subplots()
    ax2.boxplot(np.transpose(by_district_arr))

    ax2.set_title("Random With Replacement")
    ax2.set_xlabel("district")
    ax2.set_ylabel("percent Democratic")

    #fig, ax1 = plt.subplots()
    #plt.imshow(percent_dem, cmap='RdBu', interpolation='nearest')
    plt.show()
