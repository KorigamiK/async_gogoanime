import asyncio
from requests_html import AsyncHTMLSession
import os
from time import time

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
    # print(f'starting {file_name}')   
    try :
        stream_page_url = r.html.find('li.dowloads', first=True).find('a', first=True).attrs['href']
        stream_page = await assession.get(stream_page_url)
        dow_link = None
        for i in stream_page.html.find('div.dowload'):
            if option in i.text:
                # print('done')
                dow_link = i.search('href="{}"')[0]
                break
            
        return (dow_link.replace('&amp;', '&'), file_name)
    except Exception as e:
        raise e

async def gogo_downloader(get_links_coro, session: AsyncHTMLSession):
    link, episode = await get_links_coro
    print(f"{episode}\n{link}")

    # response = await session.get(link)
    # print(response.status_code)
    return f'done {episode}'

@timer
async def main(link, start, end, quality_option):
    tasks = []
    base_url = link.replace(link.split('episode-')[-1], '{}')

    for i in range(start, end+1):
        tasks.append(
            gogo_downloader(
                get_links(base_url.format(i), quality_option), assession)
                )

    result = await asyncio.gather(*tasks)
    for i in result:
        print(i)
        
    await assession.close()
    
loop = assession.loop
link = 'https://gogoanime.vc/honobono-log-episode-1'
option = '480'
loop.run_until_complete(main(link, 3, 3, option))
