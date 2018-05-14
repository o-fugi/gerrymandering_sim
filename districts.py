import matplotlib.pyplot as plt
import numpy as np

district = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
count = 0

file = open("districts.txt", 'r')

for index, line in enumerate(file, 1):
    district[count].append(float(line)/16.0)
    if index % 16 == 0 and index != 0:
        count = count + 1
    if index % 256 == 0 and index != 0:
        plt.imshow(district, cmap='Greens', interpolation='nearest')
        plt.show()
        district = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
        count = 0
