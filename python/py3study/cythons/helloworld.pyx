import math

def merc_distance(double Lon1, double Lat1, double Lon2, double Lat2):
    cdef double k
    Lat1 = Lat1 * math.pi / 180.0
    Lon1 = Lon1 * math.pi / 180.0
    Lat2 = Lat2 * math.pi / 180.0
    Lon2 = Lon2 * math.pi / 180.0
    k = math.cos(Lat1) * math.cos(Lat2) * math.cos(Lon2 - Lon1) + math.sin(Lat1) * math.sin(Lat2);
    if k > 1:
        k = 1;
    return 6378137 * math.acos(k);


def demo():
    for _ in range(10000000):
        merc_distance(103.966866, 30.562932, 103.961372, 30.559606)
