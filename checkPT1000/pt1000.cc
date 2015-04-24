#include <iostream>
#include <cstdlib>
int main(int argc, char *argv[]){

	// http://www.systemair.com/Documentation/Fans%20and%20Accessories/resistance_table_PT1000_sensors_gb.pdf
	//
	if(argv[1] == NULL) {
		std::cout<<"Please insert the resistor value like : pt1000 1089"<<std::endl;
		return 0;
	}
	float resistor = atof(argv[1]);
	std::cout<<"pT1000 with a measurement of resistor : "<<resistor<<" ohm, thus the corresponding temperature is "<<1/3.9*(resistor+23*3.9-1089.6)<<" oC"<<std::endl;
	return 0;
}
