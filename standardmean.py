from boxplots import *

num_cities = 100
target_mean = 0.5
variances = []

def adjustForMean(percent_dem, target_mean):
    print(np.mean(percent_dem.flat))
    return percent_dem + target_mean - np.mean(percent_dem.flat)


if __name__ == '__main__':
    fig, axes = plt.subplots(nrows=10,ncols=10)
    for i, ax in enumerate(axes.flat):
        i = i+1
        adjusted_percent_dem = adjustForMean(makeCityDistribution(i), target_mean)
        print(np.mean(adjusted_percent_dem.flat))
        variance = np.var(adjusted_percent_dem.flat)
        ax.axis([0.45, 0.55, 0, 100])
        ax.hist(adjusted_percent_dem.flat, bins=np.arange(.45, .55, .01))
        #make a boxplot

        variances.append(variance)

    fig, ax = plt.subplots()
    ax.set_title("variances per city, standard mean")
    ax.axis([0, num_cities + 1, 0, 0.0005])
    ax.plot(range(1, num_cities + 1), variances)
    plt.show()
