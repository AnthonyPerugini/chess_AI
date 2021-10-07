from bs4 import BeautifulSoup
import requests
import urllib.request
import os
import zipfile

# download raw
base_url = 'http://www.pgnmentor.com/'

r = requests.get(os.path.join(base_url, 'files.html'))
soup = BeautifulSoup(r.text, "html.parser")

links = set()
for link in soup.findAll("a"):
    url = link.get("href")
    if str(url).startswith('players') and str(url).endswith(".zip"):
        links.add(url)

os.chdir('/home/spicy/fun/repos/chess_AI/data/')
cwd = os.getcwd()

count = 1
for link in links:
    print(f'Processing [{count} / {len(links)}]')
    if os.path.exists(os.path.join('raw', link)):
        print(f'\tlink already exists, skipping {link}...')
    else:
        r = requests.get(os.path.join(base_url, link), allow_redirects=True)
        with open(os.path.join(cwd, 'raw', link), 'wb') as f:
            f.write(r.content)
            print(f'\t{link} successfully downloaded!')
    count += 1

# process raw
for root, dirs, files in os.walk('raw/players/'):
    for file in files:
        filename = file.split('.')[0] + '.pgn'
        if os.path.exists(os.path.join(cwd, 'processed', f'{filename}')):
            print(f'{file} already processed, skipping...')
            continue
        with zipfile.ZipFile(os.path.join(cwd, 'raw', 'players', file), "r") as zip_ref:
            zip_ref.extractall(os.path.join(cwd, 'processed'))
            print(f'Successfully unzipped {file}!')
