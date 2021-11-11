#pip install python-pdfkit
#also install wkhtmltopdf from https://wkhtmltopdf.org/
import argparse
import pdfkit
import os
def htmltopdf(m):
    listdir=os.listdir(m)
    count=0
    for i in listdir:
        n=os.listdir(os.path.join(m,i))
        for j in n:
            out=j.split(".")[0]+".pdf"
            a=os.path.join(m,i,j)
            b=os.path.join(m,i,out)
            pdfkit.from_file(a,b)
            count=count+1
    print(count)

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--path", required=True,
        help="path to directory of HTML files")
    args = vars(ap.parse_args())
    htmltopdf(args['path'])
