from pytube import YouTube
import requests
from bs4 import BeautifulSoup
import time
import pickle
import os
import moviepy.editor as mp


class YoutubeDownloader:
    def __init__(self):
        pass

    def download_youtube(self, url, path):
        try:
            yt = YouTube(url)
            l = yt.length
            if int(l) < 1000:
                n = yt.streams.first().download(path)
                print("------Downloading --[[[ {} ]]]-- Completed------".format(yt.title))
                return n
            else:
                print("FILE SIZE TOO LONG ----[[[{}]]]".format(yt.title))
                return False
        except:
            print("Error in {}".format(url))
            return False

    def update_list(self, url, ls):
        if url not in ls:
            ls.append(url)
            return ls
        else:
            return False

    def convert_audio(self, name, dpath):
        clip = mp.VideoFileClip(name)
        name = os.path.basename(name)[:-4]
        clip.audio.write_audiofile(dpath + "\\" + name + ".mp3")
        print("------Converting --[[[ {} ]]]--to .mp3 Completed------".format(name))
        clip.close()
        pass


class bollywood(YoutubeDownloader):
    def __init__(self):
        pass

    def tseries(self):
        if os.path.isfile('tseries'):
            f = open('tseries', 'rb')
            ls = pickle.load(f)
            f.close()
        else:
            ls = []
        latest = "https://www.youtube.com/user/tseries/videos?view=0&sort=dd&flow=list"
        prefix = "https://www.youtube.com"
        spath = "J:\\python_projects\\ScreenAutomate\\T-series\\video"
        dpath = "J:\\python_projects\\ScreenAutomate\\T-series\\audio"
        txt = requests.get(latest).text
        soup = BeautifulSoup(txt, "html.parser")
        for i in soup.find_all("h3", {"class": "yt-lockup-title"}):
            url = prefix + i.find('a').get('href')
            t = super().update_list(url, ls)
            if t:
                name = super().download_youtube(url=url, path=spath)
                if name:
                    super().convert_audio(name, dpath)
                ls = t
                f = open('tseries', 'wb')
                pickle.dump(ls, f)
                f.close()


class English(YoutubeDownloader):
    def __init__(self):
        pass

    def billboard(self):
        spath = "J:\\python_projects\\ScreenAutomate\\billboard\\video"
        dpath = "J:\\python_projects\\ScreenAutomate\\billboard\\audio"
        prefix = "https://www.youtube.com"
        if os.path.isfile('Billboards'):
            f = open('Billboards', 'rb')
            ls = pickle.load(f)
            f.close()
        else:
            ls = []
        billboard = requests.get("https://www.billboard.com/charts/hot-100")
        soup = BeautifulSoup(billboard.text, "html.parser")
        arr = []
        for i in soup.find_all("div", {"class": "chart-list-item__first-row chart-list-item__cursor-pointer"}):
            s = i.text
            s = s.replace("\n", " ")
            x = [u.strip() for u in s.split("  ") if u.strip() != '']
            if len(x) == 4:
                x = x[:3]
            arr.append(x)
        for a in arr:
            text = " "
            text = text.join(a[1:])
            print(text)
            txt = requests.get("https://www.youtube.com/results?search_query=" + text)
            soup = BeautifulSoup(txt.text, "html.parser")
            finder = lambda x: x.find('a', {"aria-hidden": "true", "class": "yt-uix-sessionlink spf-link"})
            link = [finder(x).get('href') for x in soup.find_all("div") if finder(x) is not None][0]
            url = prefix + link
            t = super().update_list(url, ls)
            if t:
                name = super().download_youtube(url=url, path=spath)
                if name:
                    super().convert_audio(name, dpath)
                ls = t
                f = open('Billboards', 'wb')
                pickle.dump(ls, f)
                f.close()


#c = bollywood()
#c.tseries()
#d = English()
#d.billboard()
