
import math

def merc_x(lon):
  r_major=6378137.000
  return r_major*math.radians(lon)

def merc_y(lat):
  if lat>89.5:lat=89.5
  if lat<-89.5:lat=-89.5
  r_major=6378137.000
  r_minor=6356752.3142
  temp=r_minor/r_major
  eccent=math.sqrt(1-temp**2)
  phi=math.radians(lat)
  sinphi=math.sin(phi)
  con=eccent*sinphi
  com=eccent/2
  con=((1.0-con)/(1.0+con))**com
  ts=math.tan((math.pi/2-phi)/2)/con
  y=0-r_major*math.log(ts)
  return y


def merc_ll(lng, lat):
    return merc_x(lng), merc_y(lat)


r_major = 6378137.0 # Equatorial Radius, WGS84
r_minor = 6356752.314245179#defined as constant
f = 298.257223563#// 1 / f = (a - b) / a, a = r_major, b = r_minor

def deg2rad(d):
    return d*(math.pi/180.0)

def rad2deg(r):
    return r/(math.pi/180.0)

def ll2m(lon, lat):
    x = r_major * deg2rad(lon)
    if lat > 89.5:
        lat = 89.5;
    if lat < -89.5:
        lat = -89.5;

    temp = r_minor / r_major;
    es = 1.0 - (temp * temp);
    eccent = math.sqrt(es);
    phi = deg2rad(lat);
    sinphi = math.sin(phi);
    con = eccent * sinphi;
    com = .5 * eccent;
    con2 = math.pow((1.0 - con) / (1.0 + con), com);
    ts = math.tan(.5 * (math.pi * 0.5 - phi)) / con2;
    y = 0 - r_major * math.log(ts);
    return (x , y);


def pj_phi2(ts, e):
    N_ITER = 15;
    HALFPI = math.pi / 2;
    TOL = 0.0000000001;
    eccnth = .5 * e;
    Phi = HALFPI - 2. * math.atan(ts);
    i = N_ITER;
    while True:
        con = e * math.sin(Phi);
        dphi = HALFPI - 2. * math.atan(ts * math.pow((1. - con) / (1. + con), eccnth)) - Phi;
        Phi += dphi;
        --i
        if math.fabs(dphi) < TOL or i<0:
            break
    return Phi;

def m2ll(x, y):
    lon = rad2deg((x / r_major));
    temp = r_minor / r_major;
    e = math.sqrt(1.0 - (temp * temp));
    lat = rad2deg(pj_phi2(math.exp(0 - (y / r_major)), e));
    return (lon, lat);


def distance(pt1,pt2):
    return math.sqrt(
        math.pow(pt1[0]-pt2[0], 2) + math.pow(pt1[1]-pt2[1], 2)
    )

def polygon2wkt(polygon):
    if not polygon:
        return None
    if isinstance(polygon, str):#'x y,x y,...'
        return 'POLYGON ((%s))'%polygon
    #[[x,y],[x,y],...]
    return 'POLYGON ((%s))'%','.join([ ' '.join([ str(i) for i in xy]) for xy in polygon])

        #polygon = [[[float(i)] for i in xy.split(' ')] for xy in polygon.split(',')]


def merc_distance(Lon1, Lat1, Lon2, Lat2):
    Lat1 = Lat1 * math.pi / 180.0
    Lon1 = Lon1 * math.pi / 180.0
    Lat2 = Lat2 * math.pi / 180.0
    Lon2 = Lon2 * math.pi / 180.0
    k = math.cos(Lat1) * math.cos(Lat2) * math.cos(Lon2 - Lon1) + math.sin(Lat1) * math.sin(Lat2);
    if k > 1:
        k = 1;
    return 6378137 * math.acos(k);

if __name__ == '__main__':
    print(ll2m(104.068138, 30.661796))
    print(m2ll(merc_x(104.068138), merc_y(30.661796)))
    print(polygon2wkt('1 2,3 4'))
    print(polygon2wkt([[1,2],[3,4]]))
    print(merc_distance(103.966866, 30.562932, 103.961372, 30.559606))