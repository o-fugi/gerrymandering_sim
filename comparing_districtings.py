from boxplots_heatmap import *

num_cities = 3
percent_decrease = .96
target_mean = 0.5

state = makeCityDistribution(num_cities, percent_decrease, target_mean)
# print(np.mean(state))
# plt.imshow(state, cmap='RdBu', interpolation='nearest')

boxplots_arr = assignDistricts(state) 
plt.boxplot(np.transpose(boxplots_arr))

plots_each_districting = np.transpose(boxplots_arr)
# print(plots_each_districting)

for districting in plots_each_districting:
    plt.plot(districting)

plt.show()
