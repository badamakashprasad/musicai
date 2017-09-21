import requests
from bs4 import BeautifulSoup
import urllib
import os.path
import cv
def download_mp4(path,url,name):
    name = name.replace('\n','_')
    str_name = str(path+"/"+name+".mp4")
    
    if(not(os.path.isfile(str_name))):
        urllib.urlretrieve(url,str_name)
        print("Downloading: "+name+" completed")
    else:
        print("Already downloaded "+name)
    return True

def beautifulSoup_object(url):
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text,"html5lib")
    return soup

'''
values of switch:::
songspk = 1
pagalworld = 2
mymp3songs = 3
'''
class Songspk:
    switch = 0
    def __init__(self,switch):
        self.switch = switch
        return
    def download_single(self,href,name):
        name = name.replace('\n','_')
        url = 'https://songspk.io'+href
        soup = beautifulSoup_object(url)
        soup = soup.find('div',{'class':'page-zip-wrap'})
        download_mp4("./songspk_single",soup.a.get('href'),name)
        
        
        
        return    
    def single(self):
        if self.switch == 1:
            x = 4
            while (x-=1): 
                soup = beautifulSoup_object('https://songspk.io/browse/bollywood-singles?page='+str(x))
                soup = soup.find('div',{'class':'archive-body'})
                for link in soup.findAll('figcaption'):
                    name = str(link.a.string + " by " + link.p.get_text()).replace(' ','_')
                    name = name.replace('\n','_')
                    self.download_single(link.a.get('href'),name)
                    
        return            
            
    
        

x = Songspk(1)
x.single()

    
    