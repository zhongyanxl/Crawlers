# -*- coding:utf-8 -*-
# author: nekopg
# create：2020-05-04
# update：2020-05-07
# A konachan wallpaper images crawler which to get high resolution ACG images.
import requests
from bs4 import BeautifulSoup
import os
import traceback

# download images function
def download(url, filename):
    try:
        while True:
            try:
                r = requests.get(url, timeout=10)
                r.raise_for_status()
                with open(filename + '.' + url.split('.')[-1], 'wb') as f:
                    f.write(r.content)
                return filename
            except Exception as e:
                print(e)
                print('Failed to download img')
                print('Retrying')
        
    except KeyboardInterrupt:
        if os.path.exists(filename):
            os.remove(filename)
        raise KeyboardInterrupt
    except Exception:
        traceback.print_exc()
        if os.path.exists(filename):
            os.remove(filename)
            
def start(webside, start, end):

    # Check if the folder exists, otherwise create it.
    # You can change it to change the image storage path.
    folder_path = r'imgs'
    if os.path.exists(folder_path) is False:
        os.makedirs(folder_path)


    for i in range(start, end + 1):
        while True:
            try:
                print('%d / %d' % (i, end))
                
                # Get the information of the page, and use the BeautifulSoup to parse.
                url = '%s/post?page=%d&tags=' % (webside, i)
                html = requests.get(url, timeout=10).text
                soup = BeautifulSoup(html, 'html.parser')
                
                # Find all thumbnails of the page.
                print(len(soup.find_all(class_ = "thumb")))
                for a in soup.find_all(class_ = "thumb"):
                    # Get file name
                    filename = os.path.join('imgs', a.img['src'].split('/')[-1])
                    print('filename:{}'.format(filename))
                    
                    # Continue if image exists
                    if os.path.exists(filename):
                        print('file exists!')
                        continue
                    
                    # Get high resolution image href
                    print(a['href'])
                    target_url = webside + a['href']
                    print(target_url)
                    html2 = ''
                    while True:
                        try:
                            # get href text
                            html2 = requests.get(target_url, timeout=10).text
                            break
                        except Exception as e:
                            print(e)
                            print('get html2 timeout')
                            print('Retrying')
                    # Parse
                    soup2 = BeautifulSoup(html2, 'html.parser')
                    for img in soup2.find_all('a',class_="highres-show"):
                        # Get the high resolution image download link
                        target_url2 = img['href']
                        print(target_url2)
                        filename = os.path.join('imgs', target_url2.split('/')[4])
                        # Download it
                        download(target_url2, filename)
                        break
                    else:
                        # If not, download the src.
                        img = soup2.find(id='image')
                        target_url2 = img['src']
                        print(target_url2)
                        filename = os.path.join('imgs', target_url2.split('/')[4])
                        # Download it
                        download(target_url2, filename)
                else:
                    break
            except Exception as e:
                print(e)
                print('get html timeout')
                print('Retrying')

if __name__ == '__main__':

    # Set the number of start and end pages
    start_page = 1
    end_page = 8000
    
    # You can choose one of them
    webside = r'https://konachan.com'
    # webside = r'https://konachan.net'
    
    # Start
    start(webside,start_page,end_page)
