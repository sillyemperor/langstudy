#!/usr/bin/python
# -*- coding: utf-8 -*-
import math

class vec:
    def __init__(self, pt1, pt2):
        self.pt1 = pt1
        self.pt2 = pt2
        self.x = pt2[0] - pt1[0]
        self.y = pt2[1] - pt1[1]
        self.distance = math.sqrt(math.pow(self.x, 2) + math.pow(self.y, 2))
        self.normal = self.distance and ((self.pt2[0] - self.pt1[0]) / self.distance, (self.pt2[1] - self.pt1[1]) / self.distance) or 0

    def __mul__(self, other):
        '''dot of two vector'''
        return self.x*other.x+self.y*other.y

    def __str__(self):
        return '(%s,%s)'%(self.x, self.y)


def angle(vec1, vec2):
    dot = vec1 * vec2
    dd = vec1.distance*vec2.distance
    if dd == 0:
        return 0
    k = dot/dd
    # print k, vec1, vec2
    r = math.acos(k)*180/math.pi
    if vec2.x<0:
        r += (180-r)*2
    return r


if __name__ == '__main__':
    # for i in range(0, 360, 45):
    #     print i, math.cos(i*math.pi/180), math.acos(math.cos(i*math.pi/180))*180/math.pi

    print(angle(vec([0,0], [0,10]), vec([0,0], [10,10])), 45)
    print(angle(vec([0, 0], [0, 10]), vec([0, 0], [10, 0])), 90)
    print(angle(vec([0, 0], [0, 10]), vec([0, 0], [10, -10])), 135)
    print(angle(vec([0, 0], [0, 10]), vec([0, 0], [0, -10])), 180)
    print(angle(vec([0, 0], [0, 10]), vec([0, 0], [-10, -10])), 225)
    print(angle(vec([0, 0], [0, 10]), vec([0, 0], [-10, 0])), 270)
    print(angle(vec([0, 0], [0, 10]), vec([0, 0], [-10, 10])), 315)
    # print angle(vec((11583477.533930799, 3573694.6006541513), (11583477.533930799, 3573694.6006541513+100)),
    #             vec((11583477.533930799, 3573694.6006541513), (11583471.353444744, 3573688.366794464)))
    # #135.24633316
    # print angle(vec((12959597.154878944, 4828160.598643637),(12959597.154878944, 4828160.598643637+100)),
    #             vec((12959597.154878944, 4828160.598643637),(12959587.174187522, 4828160.830448011)))
    # #88.669528549
    #
    # print angle(vec((12953642.420388581, 4835577.100773548),(12953642.420388581, 4835577.100773548+100)),
    #             vec((12953642.420388581, 4835577.100773548), (12953642.35529493, 4835572.101191323)))
    #             #269.254061517

