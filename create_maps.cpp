#include <iostream>
#include <fstream>
#include <cstdlib>
#include <vector>
#include <cmath>
#include <random>
#include <ctime>

int num_cities = 3;
int prec_dim = 10; //dimension n
float percent_dem = .6;
float percent_decrease = .9;
float dist_factor = 0.8;

struct Precinct
{
	float percent_democratic;
	int district;
};

float dist_from_city(int x, int y, std::vector< std::vector<int> > city_locations) {
	float distance = sqrt(pow((x-city_locations[0][0]), 2) + pow(y-city_locations[0][1], 2));
	for(int i = 1; i<num_cities; i++) {
		float next_dist = sqrt(pow((x-city_locations[i][0]), 2) + pow(y-city_locations[i][1], 2));
		if (distance > next_dist)
			distance = next_dist;
	}
	distance = pow(distance, dist_factor);
	//std::cout << distance << '\n';
	return distance;
}

int main(int argc, char *argv[]) {
	std::random_device random;
	std::mt19937 generator(random());
	std::uniform_int_distribution<> city_dim(0, prec_dim);

	/*
	 * NxN array of precincts
	 * randomly choose C cities (location precinct, precinct) to be P percent democratic
	 * all cities bordering that will be M percent less democratic, beyond that M less democratic, etc, until all precincts are assigned a certain percentage democratic
	 * then, districts -- assign each precinct to a district (another NxN array probably) and adjust
	 */

	std::vector< std::vector<Precinct> > precincts;
	precincts.resize(prec_dim);
	std::vector< std::vector<int> > city_locations;

	for(int i = 0; i<num_cities; i++){
		std::vector<int> city = {city_dim(generator), city_dim(generator)};
		city_locations.push_back(city);
		//std::cout << city[0] << " " << city[1] << '\n';
	}

	float tmp_percent;
	for(int i = 0; i<prec_dim; i++) {
		for(int j = 0; j<prec_dim; j++) {
			static Precinct tmp_precinct;
			tmp_percent = percent_dem * pow(percent_decrease, dist_from_city(i, j, city_locations));
			tmp_precinct.percent_democratic = ((tmp_percent<=percent_dem) ? tmp_percent : percent_dem);
			precincts[i].push_back(tmp_precinct);
			std::cout << precincts[i][j].percent_democratic << '\t';
			if(j == prec_dim - 1)
				std::cout << '\n';
		}
	}
}
