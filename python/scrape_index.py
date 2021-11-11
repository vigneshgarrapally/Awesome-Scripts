from selenium import webdriver
from time import sleep
driver = webdriver.Chrome (executable_path="C:\\Users\\vignesh\\Desktop\\chromedriver_win32\\chromedriver.exe")
driver.maximize_window()
s=input("Enter Index link")
e_links=[]
e_links.append(s)
driver.get(s)
sleep(30)
d_links=[]
def get_links(site):
    driver.get(site)
    sleep(5)
    lnks=driver.find_elements_by_tag_name("a")
    for a in lnks:
        if(a.get_attribute('class')=="list-group-item list-group-item-action"):
            e_links.append(a.get_attribute('href'))
        elif (a.get_attribute('class')=="list-group-item-action"):
            d_links.append(a.get_attribute('href'))
while len(e_links)!=0:
    get_links(e_links.pop(0))
print("Number of links are :{}".format(len(d_links)))
dest=input("Enter save filename that should be ended with .txt extension")
f=open(dest,'w')
for l in d_links:
    f.write(l+"\n")
f.close()