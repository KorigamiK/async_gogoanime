import requests
from bs4 import BeautifulSoup as bs
import subprocess
import os
dir = os.getcwd()
if os.path.isdir(dir):
    os.chdir(dir)
else:
    os.mkdir(dir)
    os.chdir(dir)
client = requests.Session()
def get_stream():
    for i in range(3,7):
        try:
            # print(f"https://gogoanime.so/saiki-kusuo-no-ps-nan-tv-episode-{i:d}")
            res = client.get(f"https://gogoanime.so/rezero-kara-hajimeru-isekai-seikatsu-2nd-season-episode-{i:d}")
            soup = bs(res.text, "html.parser")
            yield [soup.find('li', class_="dowloads").a["href"], f'ep_{i:02d}.mp4']
        except AttributeError:
            print(f'error {i}')
            # res = client.get(f"https://gogoanime.so/saiki-kusuo-no-psi-nan-episode-{i:d}")
            # soup = bs(res.text, "html.parser")
            # yield soup.find('li', class_="dowloads").a["href"]

def get_dows(link, name):
    response = bs(client.get(link).text, "html.parser")
    links = response.find_all('div', class_="dowload")
    for i in links:
        if " ".join(i.a.text.split()) == "Download (360P - mp4)":
            return [i.a["href"], name]

def downloader(link, output):
    query=f'wget "{link}" -q --show-progress --no-check-certificate -o {output}'
    subprocess.run(query,shell=True)

def download():
# with open("links.txt", "a+") as f:
    for i in get_stream():
#         downloader(*get_dows(*i))
        print(*get_dows(*i))
        # f.flush()


download()