#include <iostream>
#include <fstream>
#include <cstdlib>
#include <vector>
#include <cmath>

int num_cities = 3;
int prec_dim = 50; //dimension n
float percent_dem = .8;
float percent_decrease = .5;

struct Precinct
{
	float percent_democratic;
	int district;
};

int dist_from_city(int i, int j, std::vector< std::vector<int> > city_locations) {
	int distance = 0;
	for(int i = 0; i<city_locations.size(); i++) {
		distance += sqrt(pow((i-city_locations[i][0]), 2) + pow(j-city_locations[i][1], 2));
	}
	return distance;
}

int main(int argc, char *argv[]) {
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
		static std::vector<int> city = {static_cast<int>(rand() * prec_dim), static_cast<int>(rand() * prec_dim)};
		city_locations.push_back(city);
	}

	for(int i = 0; i<prec_dim; i++) {
		for(int j = 0; j<prec_dim; j++) {
			static Precinct tmp_precinct;
			tmp_precinct.percent_democratic = percent_dem * pow(percent_decrease, dist_from_city(i, j, city_locations));
			precincts[i].push_back(tmp_precinct);
		}
	}
}
