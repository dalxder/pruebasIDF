import urllib2
import pyPdf
import json

def main():
    with open("A Listado estaciones con IDF_actualizado a 23 mar 2017.csv") as dataEsta:
        estaciones=dataEsta.readlines()
    data=[]
    nodata=[]
    for i, estacionPdf in enumerate(estaciones):
        if i>0:
            datos=estacionPdf.split(",")
            coordenadas=datos[1:3]
            nombrePdf="IDF_"+datos[3]+"_"+datos[4].replace(" ","_")+".pdf"
            print(nombrePdf)
            try:
                download_file("http://www.ideam.gov.co/documents/10182/24541172/%s"%nombrePdf,nombrePdf)
                data.append([nombrePdf,textoPdfCoef(nombrePdf),coordenadas])
            except:
                nodata.append(nombrePdf)

        #print "procesado %i"%((i+1)/len(listaPdf)*100)
        #print data
    a=crearJson(data)
    #update()
    print(nodata)
    #geom = QgsGeometry.fromPolygon([[QgsPoint(pt[0],pt[1])  for pt in geojson['coordinates'][0] [0]]])



def download_file(download_url,nombrePdf):
    response = urllib2.urlopen(download_url)
    file = open(nombrePdf, 'wb')
    file.write(response.read())
    file.close()

def textoPdf(nombrePdf):
    pdf = pyPdf.PdfFileReader(open(nombrePdf, "rb"))
    for page in pdf.pages:
        data=[]
        a=page.extractText().split("TR=100")[1].split("Datos")[0].split(".")
        print(a)
        r=10
        for i,d in enumerate([15,30,60,120,360]):
            for j,tr in enumerate([2,3,5,10,25,50,100]):
                if j==0:
                    data.append(float(a[r*i+3+j][5:]+"."+a[r*i+4+j][0]))
                else:
                    data.append(float(a[r*i+3+j][1:]+"."+a[r*i+4+j][0]))
                #print "dURACION %i %i "%(d,tr)+ str(data[i*7+j])
    return data
def textoPdfCoef(nombrePdf):
    pdf = pyPdf.PdfFileReader(open(nombrePdf, "rb"))
    for page in pdf.pages:
        data=[]
        a=page.extractText().split("TR=100")[1].split("Datos")[0].split(".")
        r=10
        for i,d in enumerate([2,3,5,10,25,50,100]):
            #for j,tr in enumerate(["C1","X0","C2"]):
                if i<6 and i>=1:
                    C1=float(a[r*i][1+len(str(d)):]+"."+a[r*i+1][:3])


                elif i==0:
                    C1=float(a[r*i][1:]+"."+a[r*i+1][:3])
                else:
                    None
                    C1=float(a[r*(i-1)+3][1+len(str(d)):]+"."+a[r*(i-1)+4][:3])

                if i<6:
                    X0=float(a[r*i+1][3:]+"."+a[r*i+2][:3])
                    C2=float(a[r*i+2][3:]+"."+a[r*i+3][:3])
                else:
                    None
                    X0=float(a[r*(i-1)+4][3:]+"."+a[r*(i-1)+5][:3])
                    C2=float(a[r*(i-1)+5][3:]+"."+a[r*(i-1)+6][:3])
                data.append([C1,X0,C2])
    return data


def crearJson(datas):
    json=""

    tr=[2,3,5,10,25,50,100]
    coorX=4
    coorY=-74
    # itera para cada estacion
    feature=""
    for i in range(len(datas)):
        str_coef=""
        data=datas[i][1]
        nombEstacion=datas[i][0]
        #print(data[j][2][1],data[j][2][0])
        # itera para cada periodo de retorno
        for j,t in enumerate(tr):
            str_coef+='"tr%s":[%s,%s,%s]'%(t,data[j][0],data[j][1],data[j][2])
            if j<len(tr)-1:
                str_coef+=','
        feature+="""{
        "type": "Feature",
        "geometry": {
        "type": "Point",
        "coordinates": [%s, %s]
        },
        "properties": {
        "name": "%s",
        "id":["C1","X0","C2"],
        "coeficientes":{%s}
        }
        }\n"""%(datas[i][2][1],datas[i][2][0],nombEstacion,str_coef)
        if i<len(datas)-1:
            feature+=','




    featureCollection="""   {
    "type": "FeatureCollection",
    "features": [%s]}"""%(feature)
    with open("estaciones.geojson", 'wb') as createGeojson:
        createGeojson.write(featureCollection)

    return featureCollection


if __name__ == "__main__":
    main()
