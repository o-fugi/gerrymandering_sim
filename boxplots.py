import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon
import math as m

filename = 'distribution.txt'
district_dim = 4 #there are 4x4 districts

def norm(diff, norm_value):
    if diff < 0:
        diff = diff+norm_value
    return float(diff)

def assigndistricts(y_point, x_point):
    #print("districting number: ", assigndistricts.percent)
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
	    district_num = x_count + y_count*(prec_dim/district_dim) - 1
            if district_num == district_dim**2 - 1:
                pass
                #print arr[y][x]
            data[district_num][assigndistricts.percent] += arr[y][x]/((prec_dim/district_dim) ** 2)
    assigndistricts.percent += 1

#you want a 2d array, each row is a distribution (one for each districting!) for one district.


def giveDistrict(acount, districting):

    district_x = districting % district_dim #type of x-districting
    district_y = m.floor(districting / district_dim) #type of y-districting
    
    x_dim = m.floor(norm((acount%prec_dim) - district_x, prec_dim) / prec_dim * district_dim)
    y_dim = m.floor(norm(m.floor(acount/prec_dim) - district_y, prec_dim) / prec_dim * district_dim)
    
    district = x_dim + y_dim*(prec_dim/district_dim) -1
    print(district)
    return int(district) #value from 0 to district_dim**2 - 1
    

if __name__ == '__main__':
    #Takes all the elements from a file and creates an array with one row and x number of columns based on new lines
    arr = np.fromfile(filename, float,-1,"\r\n")
    #Finds the square root of the number of elements in the array and makes that the dimension
    prec_dim = int(m.sqrt(len(arr)))
    #Reshapes the array based on the dimension decided
    arr = np.reshape(arr,(prec_dim,prec_dim))

    districting_averages = np.empty([(prec_dim/district_dim)**2, district_dim**2])  #one row for each districting, 16 districts in a row

    show_districts = np.empty([prec_dim**2, 1])
    print(show_districts)

    medians = np.empty([(prec_dim/district_dim)**2])

    for d, districting in enumerate(districting_averages):
        for index, value in enumerate(np.nditer(arr)):
            show_districts[index] = float(giveDistrict(index, d)) / 8
            districting[giveDistrict(index, d)] += value
        #plt.imshow(np.reshape(show_districts, (prec_dim, prec_dim)), cmap='RdBu', interpolation='nearest')
        #plt.show()

    '''assigndistricts.percent = 0
    data = np.zeros((district_dim**2, (prec_dim/district_dim)**2)) #one row for each district (1-16) with one slot for each precinct in that district
    for y in range(0, int(prec_dim/district_dim)):
        for x in range(0, int(prec_dim/district_dim)):
            assigndistricts(y, x)'''

    #print(data)

    #data = np.transpose(data)


    rows_are_districts = np.transpose(districting_averages)
    for index, district in enumerate(rows_are_districts):
       # print(district)
        #print(np.median(district))
        medians[index] = np.median(district)
        #medians = np.append(medians, np.average(district))

    medians = np.asarray(medians)

    print(len(medians))

    print(medians)
    meaninds = medians.argsort()
    print(meaninds)
    rows_are_districts = rows_are_districts[meaninds]
    districting_averages = np.transpose(rows_are_districts)

    fig, ax = plt.subplots()
    districting_averages = np.divide(districting_averages, (prec_dim/district_dim)**2)
    ax.boxplot(districting_averages)

    fig, ax1 = plt.subplots()
    percent_dem = arr

    plt.imshow(percent_dem, cmap='RdBu', interpolation='nearest')
    plt.show()
