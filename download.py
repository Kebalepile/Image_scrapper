import json
import requests as req
import os


# opening JSON file
with open('scrape_links.json', 'r') as openfile:
    global f
    f = json.load(openfile)


def folder_name():
    name = input(':: Enter desired folder name: ')
    if len(name) > 0:
        return name
    return folder_name()


name = folder_name()

path = f'./downloads/{name}'

count = 0


def scrape_img(file_extension, content):
    global count
    with open(os.path.join(path, f'{name + str(count)}.{file_extension}'), 'wb') as img:
        img.write(content)
    count += 1


if not os.path.exists(path):
    os.makedirs(path)

print('\t .......Downloading images........\n\t ..........it may take a while')

for k, v in f.items():
    r = req.get(v)
    assert r.status_code == 200, f'recevied a {r.status_code} status code.'
    t = r.headers['Content-Type'][6:]
    scrape_img(t, r.content)

print(f'::  Done check {path}')
