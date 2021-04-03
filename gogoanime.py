import asyncio
from requests_html import AsyncHTMLSession
import os
from time import time
from async_subprocess import async_subprocess

try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except:
    pass

def timer(function):
    async def wrapped_func(*args):
        s = time()
        res = await function(*args)
        print(f'{function.__name__} took {time()-s} seconds')
        return res
    return wrapped_func

dir = os.getcwd()#set it to whatever you want
if os.path.isdir(dir):
    os.chdir(dir)
else:
    os.mkdir(dir)
    os.chdir(dir)
    
assession = AsyncHTMLSession()

async def get_links(link, option):
    r = await assession.get(link) 
    # print(r.html.find('a[target="_blank"]')[-1].attrs['href'])
    file_name = link.split('/')[-1].replace('-', ' ')
    try :
        stream_page_url = r.html.find('li.dowloads', first=True).find('a', first=True).attrs['href']
        stream_page = await assession.get(stream_page_url)
        dow_link = None
        for i in stream_page.html.find('div.dowload'):
            if option in i.text:
                dow_link = i.search('href="{}"')[0]
                break
        return (dow_link.replace('&amp;', '&'), file_name)
    except Exception as e:
        print(file_name, e)
        return (None, file_name)

async def download(name, link):
    return await async_subprocess(*['bash' ,'-c' ,f'curl -o "{name}" "{link}"'], description=name, print_stderr=False)

async def gogo_downloader(get_links_coro):
    link, episode = await get_links_coro
    if not link:
        return f'cannot download {episode.split("episode")[-1]}'
    await download(episode+'.mp4', link)
    return f'done {episode.split("episode")[-1]}'

@timer
async def main(link, iterator, quality_option):
    tasks = []
    base_url = link.replace(link.split('episode-')[-1], '{}')

    for i in iterator:
        tasks.append(gogo_downloader(get_links(base_url.format(i), quality_option)))

    result = await asyncio.gather(*tasks)
    for i in result:
        print(i)
        
    await assession.close()
    
loop = assession.loop
link = 'https://gogoanime.vc/kanojo-okarishimasu-petit-episode-1'
option = '480'
ep_range = range(1, 20)
loop.run_until_complete(main(link, ep_range, option))
