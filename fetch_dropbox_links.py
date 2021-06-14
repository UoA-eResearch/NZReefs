#!/usr/bin/env python

import requests
import re
from tqdm import tqdm
import csv

with open("dropbox_links.txt") as f:
    links = f.read().splitlines()

regex = re.compile(r'"(https://[^"]+.previews.dropbox[^"]+)')

with open("dropbox_links.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerow(["link", "thumbnail"])
    for link in tqdm(links):
        req = requests.get(link.replace("https://dl", "https://www"))
        thumbnail = regex.search(req.text).groups()[0].replace("\\u0026", "&")
        writer.writerow([link, thumbnail])