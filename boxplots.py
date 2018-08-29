import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon
import math as m
import sys
import random

#constants
filename = 'distribution.txt'
prec_dim_x = 20
prec_dim_y = 20
district_dim_x = 4 #there are 4x4 districts
district_dim_y = 4 #there are 4x4 districts
num_cities = 5
dist_factor = .7
most_democratic = .57
percent_decrease = .96
weighted = False # not realistically able to be used

#globals
percent_dem = np.zeros([prec_dim_y, prec_dim_x])
population = np.zeros([prec_dim_y, prec_dim_x])

#TODO:  population density in urban areas -- test with gradient instead of with city limits
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

def makeCityDistribution(num_cities, percent_decrease):
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

    # fig, ax = plt.subplots()
    # plt.imshow(population, cmap='Greys', interpolation='nearest')
    # plt.show()

    return percent_dem

# def makeSeparatedDistribution(separate_value):
#     percent_dem = np.random.rand(prec_dim_y, prec_dim_x)
#     fig, ax1 = plt.subplots()
#     plt.imshow(percent_dem, cmap='RdBu', interpolation='nearest')
#     plt.show()
# 
#     separated = False
#     temp_percent = 0
#     count = 0
#     means = []
#     avgs = []
# 
#     while(!separated):
#         count += 1
#         city_generate = [[random.randint(0, prec_dim_y - 1), random.randint(0, prec_dim_x - 1)] for city in range(0, num_cities)]
#         for city in city_generate:
#             city_percent = percent_dem[city[0], city[1]]
#             dist_area = int(min(prec_dim_y, prec_dim_x) * abs(0.5-city_percent)) + 1
#             
#             for num in range(0, district_dim_x*district_dim_y): 
#                 x1 = int((num%district_dim_x)*(prec_dim_x/district_dim_x))
#                 y1 = int(m.floor(num/district_dim_y)*prec_dim_y/district_dim_y)
#                 dist_box = np.take(np.roll(np.take(np.roll(percent_dem, y1, axis=1), range(0, dist_area), axis=1), x1, axis=0), range(0,dist_area), axis=0)
#                 avgs.append(np.average(dist_box))
# 
#             if city_percent > 0.5:
#                 max_dist = avgs
# 
#             """x1 = int(wrap(city[0] - 3, prec_dim_x))
#             x2 = int(wrap(city[0] + 3, prec_dim_x))
#             y1 = int(wrap(city[1] - 3, prec_dim_y))
#             y2 = int(wrap(city[1] + 3, prec_dim_y))
#             dist_box = np.take(np.roll(np.take(np.roll(percent_dem, y1, axis=1), range(0, 3), axis=1), x1, axis=0), range(0,3), axis=0)"""
# 
#             # finds the precinct with closest value to its own and sticks onto that
#             diff = np.abs(dist_box-percent_dem[city[0], city[1]])
#             closest_idx = np.where(diff==diff.min())
#             temp_percent = percent_dem[closest_idx[0], int(wrap(closest_idx[1] + 1, prec_dim_y))]
#             percent_dem[closest_idx[0], int(wrap(closest_idx[1] + 1, prec_dim_y))] = percent_dem[city[0], city[1]]
#             percent_dem[city[0], city[1]] = temp_percent 
# 
#         mean = np.mean(np.abs(percent_dem - np.roll(percent_dem, 1, axis=0)))
#         means.append(mean)
#         if(separated): #will soon become if something > separated_values
#             separated = True
# 
#         if count % 400  == 0:
#             fig, ax = plt.subplots()
#             ax.plot(means)
#         if count % 50 == 0:
#             fig, ax1 = plt.subplots()
#             plt.imshow(percent_dem, cmap='RdBu', interpolation='nearest')
#             plt.show()
# 
#     return percent_dem

def randomWithoutReplacement(arr):
    arr = np.reshape(arr, arr.size)
    np.random.shuffle(arr)
    arr = np.reshape(arr, (prec_dim_y, prec_dim_x))

    return arr

def randomWithReplacement(arr):
    copy = arr.flat
    for i, element in enumerate(arr.flat):
        arr.flat[i] = np.random.choice(copy)

    return arr

def assignDistricts(percent_dem):
    by_district_arr = np.zeros([int(district_dim_x*district_dim_y), int(prec_dim_x/district_dim_x*prec_dim_y/district_dim_y)]) # each row is one district, each column is one districting
    for num, district in enumerate(by_district_arr): 
        for d, districting in enumerate(district):
            x1 = int(d % (prec_dim_x/district_dim_x) + (num%district_dim_x)*(prec_dim_x/district_dim_x))
            x2 = int(x1 + prec_dim_x/district_dim_x)
            y1 = int(m.floor(d / (prec_dim_x/district_dim_x)) + m.floor(num/district_dim_y)*prec_dim_y/district_dim_y)
            y2 = int(y1 + prec_dim_y/district_dim_y)
            dist_box = np.take(np.take(percent_dem, range(y1, y2), axis=0, mode='wrap'), range(x1, x2), axis=1, mode='wrap') #this has a pretty serious error please fix
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

def showCities():
    percent_dem = makeCityDistribution(num_cities)
    percent_dem_copy = percent_dem
    by_district_arr = assignDistricts(percent_dem)

    by_district_arr = np.sort(by_district_arr, axis=0)
    print("making the plots")
    organized_medians = [np.median(district) for district in by_district_arr]
    fig, ax = plt.subplots()
    ax.boxplot(np.transpose(by_district_arr))

    ax.set_title("Organized into Cities")
    ax.set_xlabel("district")
    ax.set_ylabel("percent Democratic")
    ax.axis([1, district_dim_x*district_dim_y, 0.48, 0.55])

    #fig, ax1 = plt.subplots()
    #plt.imshow(percent_dem, cmap='RdBu', interpolation='nearest')

    ### RANDOM WITHOUT REPLACEMENT ###

    percent_dem = randomWithoutReplacement(percent_dem)
    by_district_arr = assignDistricts(percent_dem)

    by_district_arr = np.sort(by_district_arr, axis=0)
    print("making the plots")
    wout_replacement_medians = [np.median(district) for district in by_district_arr]
    fig, ax1 = plt.subplots()
    ax1.boxplot(np.transpose(by_district_arr))

    ax1.set_title("Random Without Replacement")
    ax1.set_xlabel("district")
    ax1.set_ylabel("percent Democratic")
    ax1.axis([1, district_dim_x*district_dim_y, 0.48, 0.55])

    #fig, ax1 = plt.subplots()
    #plt.imshow(percent_dem, cmap='RdBu', interpolation='nearest')

    ### RANDOM WITH REPLACEMENT ###

    percent_dem = randomWithReplacement(percent_dem)
    by_district_arr = assignDistricts(percent_dem)

    by_district_arr = np.sort(by_district_arr, axis=0)
    print("making the plots")
    w_replacement_medians = [np.median(district) for district in by_district_arr]
    fig, ax2 = plt.subplots()
    ax2.boxplot(np.transpose(by_district_arr))

    ax2.set_title("Random With Replacement")
    ax2.set_xlabel("district")
    ax2.set_ylabel("percent Democratic")
    ax2.axis([1, district_dim_x*district_dim_y, 0.48, 0.55])

    #fig, ax1 = plt.subplots()
    #plt.imshow(percent_dem, cmap='RdBu', interpolation='nearest')

    ### BOXPLOT VARIANCES ###

    diffs = [a-b for (a, b) in zip(w_replacement_medians, wout_replacement_medians)]
    print(diffs)

    variances = np.sum([(a-b)**2 for a, b in zip(organized_medians, wout_replacement_medians)])
    print("organized and wout replacement: %f" % variances)
    variances = np.sum([(a-b)**2 for a, b in zip(organized_medians, w_replacement_medians)])
    print("organized and w replacement: %f" % variances)
    variances = np.sum([(a-b)**2 for a, b in zip(w_replacement_medians, wout_replacement_medians)])
    print("w and wout replacement: %f" % variances)

    plt.show()


if __name__ == '__main__':
    if(len(sys.argv) > 1):
        showDistricts()
        
    showCities()

    #percent_dem = makeSeparatedDistribution(1)
    #print(percent_dem)
