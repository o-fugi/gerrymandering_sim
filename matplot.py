import matplotlib.pyplot as plt
import numpy as np

percent_dem = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
count = 0

file = open("distribution.txt", 'r')
for index, line in enumerate(file, 1):
    percent_dem[count].append(float(line))
    if index % 16 == 0 and index != 0:
        count = count + 1

for i in range(16):
    print(percent_dem[i])

#a = np.random.random((16, 16))
plt.imshow(percent_dem, cmap='RdBu', interpolation='nearest')
plt.show()

