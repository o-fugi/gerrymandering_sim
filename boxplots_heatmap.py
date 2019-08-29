import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon
import math as m
import sys
import random
from scipy import stats

#constants
prec_dim_x = 20
prec_dim_y = 20
district_dim_x = 4 #there are 4x4 districts
district_dim_y = 4 #there are 4x4 districts
dist_factor = .7
most_democratic = .57

#globals
percent_dem = np.zeros([prec_dim_y, prec_dim_x])
population = np.zeros([prec_dim_y, prec_dim_x])

# helper functions for makeCityDistribution
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

# input of num_cities, percent_decrease, and target_mean, output of map
def makeCityDistribution(num_cities, percent_decrease, target_mean):
    global percent_dem
    city_locations = np.empty([num_cities, 2])
    for city in city_locations:
        city[0] = random.randint(0, prec_dim_x - 1)
        city[1] = random.randint(0, prec_dim_y - 1)
    
    for y, row in enumerate(percent_dem):
        for x, column in enumerate(row):
            factor = distFromCity(y, x, city_locations)
            row[x] = m.pow(percent_decrease, factor)

    percent_dem *= target_mean/np.mean(percent_dem)
    return percent_dem

# input of map, output of np.array where every row is a district
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
            district[d] = np.average(dist_box)
    return by_district_arr

# run example: create map and boxplot for that map
def runExample():
    state = makeCityDistribution(4, .96, 0.5)
    boxplot_arr = assignDistricts(state)

    boxplot_arr = np.sort(boxplot_arr, axis=0)
    organized_medians = [np.median(district) for district in boxplot_arr]
    fig, ax = plt.subplots()
    ax.boxplot(np.transpose(boxplot_arr))

    ax.set_xlabel("district")
    ax.set_ylabel("percent Democratic")
    ax.axis([1, district_dim_x*district_dim_y, 0.45, 0.55])
    plt.show()
    plt.imshow((state), cmap='RdBu', interpolation='nearest')
    plt.show()

# heatmap example: create a lot of maps with heatmaps for slope and linearity of boxplots
def heatmapExample():
    num_cities = 1 # for now

    dem_percents = np.zeros([50, 70])
    votes_won = np.zeros([50, 70]) 
    slopes = np.zeros([50, 70])
    r_values = np.zeros([50, 70])

    for a, intensity in enumerate(np.arange(0.5, 1.0, 0.01)): 
        print("a = %f" % a)
        for b, target_mean in enumerate(np.arange(.2, .9, .01)):
            # this is for one possible mapping
            state = makeCityDistribution(num_cities, intensity, target_mean)
            # how many Democrats in this mapping?
            dem_percents[a][b] = np.mean(state.flat)
            boxplot_arr = assignDistricts(state)
            boxplot_arr = np.sort(boxplot_arr, axis=0)
            # in the average (boxplot) scenario of districtings, how many Democratic votes are won?
            distr_medians = [np.median(district) for district in boxplot_arr]
            votes = 0
            for median in distr_medians:
                if median > 0.5:
                    votes += 1
            votes_won[a][b] = votes
            # slope of final boxplot -- vote per district (arbitrary comparison units, essentially)
            lin_regress = stats.linregress(range(0, len(distr_medians)), distr_medians)
            slopes[a][b] = lin_regress.slope
            r_values[a][b] = lin_regress.rvalue

    ax1 = plt.subplot(2, 2, 1)
    ax1.set_title("means")
    plt.imshow((dem_percents), cmap='RdBu', interpolation='nearest')

    ax2 = plt.subplot(2, 2, 2)
    ax2.set_title("votes_won")
    plt.imshow((votes_won), cmap='RdBu', interpolation='nearest')

    ax3 = plt.subplot(2, 2, 3)
    ax3.set_title("slopes")
    plt.imshow((slopes), cmap='RdBu', interpolation='nearest')

    ax4 = plt.subplot(2, 2, 4)
    ax4.set_title("r_values")
    plt.imshow((r_values), cmap='RdBu', interpolation='nearest')

    plt.show()

runExample()
heatmapExample()
