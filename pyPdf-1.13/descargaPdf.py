import urllib2
import pyPdf


def main():
    nombrePdf="IDF_16035010_TIBU.pdf"
    listaPdf=[nombrePdf,"IDF_11135010_SAUTATA.pdf"]
    for i, estacionPdf in enumerate(listaPdf):
        download_file("http://www.ideam.gov.co/documents/10182/24541172/%s"%estacionPdf,estacionPdf)
        data=textoPdf(estacionPdf)
        print "procesado %i"%((i+1)/len(listaPdf)*100)
        print data
        
 
    
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
        r=10
        for i,d in enumerate([15,30,60,120,360]):
            for j,tr in enumerate([2,3,5,10,25,50,100]):
                if j==0:
                    data.append(float(a[r*i+3+j][5:]+"."+a[r*i+4+j][0]))
                else:
                    data.append(float(a[r*i+3+j][1:]+"."+a[r*i+4+j][0]))
                #print "dURACION %i %i "%(d,tr)+ str(data[i*7+j])
    return data

if __name__ == "__main__":
    main()