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
float percent_decrease = .94;
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

float dist_from_city(int y, int x, std::vector< std::vector<int> > city_locations) {
	float distance = 1000000000000;
	for(int i = 0; i<num_cities; i++) {
		distance = MIN(distance, sqrt(pow(norm(x - city_locations[i][0]), 2) + pow(norm(y - city_locations[i][1]), 2)));
	}
	distance = pow(distance, dist_factor);
	return distance;
}

void assign_districts(std::vector< std::vector<Precinct> > &precincts, int y_point, int x_point, std::ofstream &file2) {
	//for every district within this mapping, assign
	/*
	 * Cycle through every precinct. First, assign precincts to 1 until x is reached.
	 * Then, assign precincts to 2 until x + district/precinct is reached. Then, assign precincts to 3 until x + district/precinct*2 is reached
	 * When x + district/precinct*(count-1) is greater than precincts divided by districts, then it's 1 again.
	 * Do basically the same thing for y, and multiply by three.
	 * */
	int x_count = 1;
	int y_count = 1;
	bool x_lapsed = false;
	bool y_lapsed = false;
	for(int y = 0; y < prec_dim; y++) {
		x_count = 1;
		x_lapsed = false;
		if (y_point + prec_dim/district_dim * (y_count-1) <= y && !y_lapsed)
			y_count++;
		if (y_count > district_dim) {
			y_count = 1;
			y_lapsed = true;
		}
		for(int x = 0; x < prec_dim; x++) {
			if (x_point + prec_dim/district_dim * (x_count-1) <= x && !x_lapsed)
				x_count++;
			if (x_count > district_dim) {
				x_count = 1;
				x_lapsed = true;
			}
			precincts[y][x].district = x_count + y_count*(prec_dim/district_dim - 1);
			file2 << x_count + y_count*(prec_dim/district_dim - 1) << '\n';
		}
	}
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

	std::ofstream file2;
	file2.open ("districts.txt");

	for(int num = 0; num<num_cities; num++){
		std::vector<int> city = {city_dim(generator), city_dim(generator)};
		city_locations.push_back(city);
		std::cout << city_locations[num][0] << " " << city_locations[num][1] << '\n';
	}
	

	for(int y = 0; y<prec_dim; y++) {
		for(int x = 0; x<prec_dim; x++) {
			static Precinct tmp_precinct;
			float factor = dist_from_city(y, x, city_locations);
			tmp_precinct.percent_democratic = COERCE(percent_dem * pow(percent_decrease, factor), 0, percent_dem);
			precincts[y].push_back(tmp_precinct);
			/*if(y<8)
				precincts[y][x].percent_democratic = 0;
			else
				precincts[y][x].percent_democratic = 1;*/
			std::cout << 100* precincts[y][x].percent_democratic << '\t';
			file << precincts[y][x].percent_democratic << '\n';
			if(x == prec_dim - 1)
				std::cout << '\n';
		}
	}

	//for every possible assigning of districts
	for(int y = 0; y<prec_dim/district_dim; y++){
		for(int x = 0; x<prec_dim/district_dim; x++) {
			assign_districts(precincts, y, x, file2);
		}
	}
}
