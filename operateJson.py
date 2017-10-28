#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      dalxder
#
# Created:     26/10/2017
# Copyright:   (c) dalxder 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

def main():
    data=jsonQuery()
    coor=[]
    print(len(data["features"]),a["features"][0]["geometry"]["coordinates"])
    for i, feat in enumerate(data["features"]):
        coor.append(feat[i]["geometry"]["coordinates"])

def jsonQuery():
    with open('estaciones.geojson') as data_file:
        data = json.load(data_file)
    return data

def objectDistance():
    distance = QgsDistanceArea()
    crs = QgsCoordinateReferenceSystem()
    crs.createFromSrsId(4326) # EPSG:4326
    distance.setSourceCrs(crs)
    distance.setEllipsoidalMode(True)
    distance.setEllipsoid('WGS84')
    return distance
	 # ~322.48m.

def distance2point(puntos):
    d=objectDistance()
    distancias=[]
    for i in range(len(puntos)):
        distancias.append(d.measureLine(QgsPoint(pointRef[0],pointRef[1]),QgsPoint(puntos[i][0],puntos[i][0])) )
    return distancias
if __name__ == '__main__':
    main()
