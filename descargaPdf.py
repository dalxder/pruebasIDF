import urllib2
import pyPdf
import json
"""
from pprint import pprint

with open('data.json') as data_file:
    data = json.load(data_file)
pprint(data)
"""
def main():
    nombrePdf="IDF_16035010_TIBU.pdf"
    listaPdf=[nombrePdf,"IDF_11135010_SAUTATA.pdf"]
    data=[]
    for i, estacionPdf in enumerate(listaPdf):
        download_file("http://www.ideam.gov.co/documents/10182/24541172/%s"%estacionPdf,estacionPdf)
        data.append([estacionPdf,textoPdfCoef(estacionPdf)])
        #print "procesado %i"%((i+1)/len(listaPdf)*100)
        #print data
    a=crearJson(data)
    print(a)
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
    for i in range(len(datas)):
        str_coef=""
        data=datas[i][1]
        nombEstacion=datas[i][0]
        for j,t in enumerate(tr):
            str_coef+='"tr%s":[%s,%s,%s]'%(t,data[j][0],data[j][1],data[j][2])
            if j<len(tr)-1:
                str_coef+=','

        template="""{
     "type": "Feature",
     "geometry": {
        "type": "Point",
        "coordinates": [125.6, 10.1]
      },
     "properties": {
       "name": "%s",
       "id":["C1","X0","C2"],
       "coeficientes":{%s}
     }
}\n"""%(nombEstacion,str_coef)
        json+=template
    return json
if __name__ == "__main__":
    main()
