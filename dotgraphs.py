from boxplots import *
from scipy import stats
import standardmean

num_cities = 1
prec_dim_x = 20
prec_dim_y = 20

dem_percents = [[]]*10 
votes_won = [[]]*10 
slopes = [[]]*10
r_values = [[]]*10

for idx, intensity in enumerate(np.arange(0.5, 1.0, 0.05)): 
    for target_mean in np.arange(.2, .9, .1) :
        # this is for one possible mapping
        percent_dem = makeCityDistribution(num_cities, intensity)
        percent_dem = standardmean.adjustForMean(percent_dem, target_mean) # this is giving wrong data, fix
        # how many Democrats in this mapping?
        dem_percents[idx].append(np.mean(percent_dem.flat))
        by_district_arr = assignDistricts(percent_dem)
        by_district_arr = np.sort(by_district_arr, axis=0)
        # in the average (boxplot) scenario of districtings, how many Democratic votes are won?
        distr_medians = [np.median(district) for district in by_district_arr]
        votes = 0
        for median in distr_medians:
            if median > 0.5:
                votes += 1
        votes_won[idx].append(votes)
        # slope of final boxplot -- vote per district (arbitrary comparison units, essentially)
        lin_regress = stats.linregress(range(0, len(distr_medians)), distr_medians)
        slopes[idx].append(lin_regress.slope)
        r_values[idx].append(lin_regress.rvalue)

# plt.subplot(2, 2, 1)
# plt.imshow((dem_percents), cmap='RdBu', interpolation='nearest')
# 
# plt.subplot(2, 2, 2)
# plt.imshow((votes_won), cmap='RdBu', interpolation='nearest')
# 
# plt.subplot(2, 2, 3)
# plt.imshow((slopes), cmap='RdBu', interpolation='nearest')
# 
# plt.subplot(2, 2, 4)
# plt.imshow((r_values), cmap='RdBu', interpolation='nearest')

fig, ax = plt.subplots()
plt.imshow((dem_percents), cmap='RdBu', interpolation='nearest')

plt.show()

