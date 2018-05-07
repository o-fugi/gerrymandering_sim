import matplotlib.pyplot as plt
import numpy as np

percent_dem = [[], [], [], [], [], [], [], [], []]
count = -1

file = open("distribution.txt", 'r')
for index, line in enumerate(file, 1):
    if index % 9 == 0:
        count = count + 1
    percent_dem[count].append(float(line))

print(percent_dem[2][3])

#a = np.random.random((16, 16))
plt.imshow(percent_dem, cmap='hot', interpolation='nearest')
plt.show()

