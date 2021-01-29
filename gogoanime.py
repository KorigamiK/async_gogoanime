import asyncio
from requests_html import AsyncHTMLSession
import os
try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except:
    pass

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
    print(f'starting {file_name}')   
    stream_page_url = r.html.find('li.dowloads', first=True).find('a', first=True).attrs['href']
    stream_page = await assession.get(stream_page_url)
    dow_link = None
    for i in stream_page.html.find('div.dowload'):
        if option in i.text:
            print('done')
            dow_link = i.search('href="{}"')[0]
            break

    return (dow_link, file_name)

def downloader(link, output):
    print(link, output)

async def main(link, start, end, quality_option):
    tasks = []
    base_url = link.replace(link.split('episode-')[-1], '{}')
    for i in range(start, end+1):
        tasks.append(get_links(base_url.format(i), quality_option))
    dow_links = await asyncio.gather(*tasks)
    for i in dow_links:
        # print(*i)
        downloader(*i)
        
    await assession.close()
    
loop = assession.loop
link = 'https://gogoanime.so/k-on-2-episode-1'
option = '360'
loop.run_until_complete(main(link, 26, 27, option))
