from boxplots import *

np.random.seed(3429034)
means = []
variances = []
max_cities = 100

if __name__ == "__main__":
    fig, axes = plt.subplots(nrows=int(m.sqrt(100)), ncols=int(m.sqrt(100)))
    for num_cities, ax in enumerate(axes.flat):
        num_cities = num_cities + 1
        city_distribution = makeCityDistribution(num_cities)
        by_district_arr = assignDistricts(city_distribution)
        ax.set_title("Normed, Number of Cities = %d" % num_cities)
        ax.axis([0.45, 0.55, 0, 100])
        n, bins, patches = ax.hist(by_district_arr.flat, bins=np.arange(.45, .55, .01))
        
        mean = np.mean(by_district_arr.flat)
        variance = np.var(by_district_arr.flat)

        #avg_bins = 0.5 * (bins[1:]+bins[:bins.size-1])
        #mean = np.sum(n*avg_bins)
        #print(mean)
        #print(mean - 100*np.mean(by_district_arr))
        means.append(mean)
        variances.append(variance)
        

    fig, axes2 = plt.subplots()
    axes2.set_title("means per city")
    axes2.plot(range(1, max_cities + 1), means)
    fig, ax = plt.subplots()
    ax.set_title("variances per city")
    ax.plot(range(1, max_cities + 1), variances)
    plt.show()

    #plot variance over num_cities and mean over num_cities for organized and random w/out replacement
