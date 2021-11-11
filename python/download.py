import os
from urllib.parse import unquote
import requests
user, password = 'goc', 'goc'
count=0
p="E:\\AI and python\\appledai"
s="https://v7.gocindex.workers.dev/0:/[Padhai%20One%20Fourth%20Labs]%20Data%20Science/Week%201-%20Introduction/10.%20Are%20AI%20and%20Data%20Science%20related%23-studyfevertelegamtelegram-gameofcourses.mp4?a=view"
if(s.find('?')>0):
  s=s.split('?')[0]
  url = unquote(s)
  outpath=os.path.join(p,*url.split('/')[4:-1])
  out_name=os.path.join(outpath,url.split('/')[-1])
  print(out_name)
  if not os.path.isfile(out_name):
    os.makedirs(outpath,exist_ok=True)
    r = requests.get(url,auth=(user, password))
    open("E:\\AI and python\\appledai\\abc.mp4", 'wb').write(r.content)
    count=count+1