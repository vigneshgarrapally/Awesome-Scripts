from PyPDF2 import PdfFileMerger
import os
m=input()
listdir=os.listdir(m)
count=0
for i in listdir:
    path=os.path.join(m,i)
    pdfs = [a for a in os.listdir(path) if a.endswith(".pdf")]
    #print(pdfs)
    merger = PdfFileMerger()
    for pdf in pdfs:
        merger.append(os.path.join(m,i,pdf))
        output=os.path.join(m,i+".pdf")
        #print(output)
    merger.write(output)
        #with open(output, "wb") as fout:
            #merger.write(fout)
    count=count+1
    merger.close()
print(count)
