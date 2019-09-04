#include <math.h>
#include <stdio.h>
#define PI 3.1415726

double merc_distance(double Lon1, double Lat1, double Lon2, double Lat2) {
    double k = 0;
    Lat1 = Lat1 * PI / 180.0;
    Lon1 = Lon1 * PI / 180.0;
    Lat2 = Lat2 * PI / 180.0;
    Lon2 = Lon2 * PI / 180.0;
    k = cos(Lat1) * cos(Lat2) * cos(Lon2 - Lon1) + sin(Lat1) * sin(Lat2);
    if(k > 1)
        k = 1;
    return 6378137 * acos(k);
}


int main() {
    for(int i=0; i< 10000000; ++i) {
        merc_distance(103.966866, 30.562932, 103.961372, 30.559606);
    }
    return 0;
}