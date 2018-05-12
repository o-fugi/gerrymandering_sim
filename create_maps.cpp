#include <iostream>
#include <fstream>
#include <cstdlib>
#include <vector>
#include <cmath>
#include <random>
#include <ctime>
#define MIN(a, b) ((a<b) ? a : b)
#define COERCE(a, min, max) ((a<min) ? min : ((a>max) ? max : a))

int num_cities = 4;
float prec_dim = 16.0; //dimension n
float percent_dem = .6;
float percent_decrease = .9;
float dist_factor = 0.8;
int district_dim = 4; //district_dim ^ 2 = number of districts

struct Precinct
{
	float percent_democratic;
	int district;
};

//this is so that the state wraps around itself
float norm(int diff) {
	diff = ((fabs(diff)>prec_dim/2) ? prec_dim - fabs(diff) : diff);
	return diff;
}

float dist_from_city(int x, int y, std::vector< std::vector<int> > city_locations) {
	float distance = 1000000000000;
	for(int i = 0; i<num_cities; i++) {
		distance = MIN(distance, sqrt(pow(norm(x-city_locations[i][0]), 2) + pow(norm(y - city_locations[i][1]), 2)));
	}
	distance = pow(distance, dist_factor);
	return distance;
}

void assign_districts(std::vector< std::vector<Precinct> > &precincts, int x, int y) {
	//for every district within this mapping, assign
	//for(int i = 0; i < prec_dim; i++) {
	//	for(int j = 0; j < prec_dim; j++) {
	//		precinct[i][j].district = floor(x/i) + 3*(1-floor(y
}	

int main(int argc, char *argv[]) {
	//note to self: j is horizontal and i is vertical!
	std::random_device random;
	std::mt19937 generator(random());
	std::uniform_int_distribution<> city_dim(0, prec_dim - 1);

	/*
	 * NxN array of precincts
	 * randomly choose C cities (location precinct, precinct) to be P percent democratic
	 * all cities bordering that will be M percent less democratic, beyond that M less democratic, etc, until all precincts are assigned a certain percentage democratic
	 * then, districts -- assign each precinct to a district (another NxN array probably) and adjust
	 */

	std::vector< std::vector<Precinct> > precincts;
	precincts.resize(prec_dim);
	std::vector< std::vector<int> > city_locations;

	std::ofstream file;
	file.open ("distribution.txt");

	//std::vector<int> test_city = {2, 8};
	//city_locations.push_back(test_city);

	for(int i = 0; i<num_cities; i++){
		std::vector<int> city = {city_dim(generator), city_dim(generator)};
		city_locations.push_back(city);
		//std::cout << city[0] << " " << city[1] << '\n';
	}
	
	//city_locations = {{7, 10}, {3, 6}, {15, 2}, {6, 6}};


	for(int i = 0; i<3; i++) {
		std::cout << city_locations[i][0] << " " << city_locations[i][1] << '\n';
	}

	for(int i = 0; i<prec_dim; i++) {
		for(int j = 0; j<prec_dim; j++) {
			static Precinct tmp_precinct;
			if(i==0 && j==2)
				std::cout << "we're here!";
			float factor = dist_from_city(i, j, city_locations);
			tmp_precinct.percent_democratic = COERCE(percent_dem * pow(percent_decrease, factor), 0, percent_dem);
			precincts[i].push_back(tmp_precinct);
			std::cout << 100* precincts[i][j].percent_democratic << '\t';
			file << precincts[i][j].percent_democratic << '\n';
			if(j == prec_dim - 1)
				std::cout << '\n';
		}
	}

	//for every possible assigning of districts
	for(int x = 0; x<prec_dim/district_dim; x++){
		for(int y = 0; y<prec_dim/district_dim; y++) {
			assign_districts(precincts, x, y);
		}
	}
}
