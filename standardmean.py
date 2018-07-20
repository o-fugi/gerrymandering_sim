from boxplots import *

target_mean = 0.5

def adjustForMean(percent_dem, target_mean):
    mean = np.mean(percent_dem.flat)


if __name__ == '__main__':
    for i in range(1, 7):
        adjusted_percent_dem = adjustForMean(makeCityDistributions(i), target_mean)
