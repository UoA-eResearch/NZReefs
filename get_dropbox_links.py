#!/usr/bin/env python3

# This script uses Dropbox's Python API to fetch shared links for each file in a shared folder

from dropbox import Dropbox
from dropbox.files import SharedLink, FolderMetadata
import os
from tqdm import tqdm
from tqdm.contrib.concurrent import thread_map

# From https://www.dropbox.com/developers/apps
DROPBOX_TOKEN = os.environ["DROPBOX_TOKEN"]
SHARED_LINK = "https://www.dropbox.com/sh/qtgta9trakhwarm/AACI70fgFHYOYexvsdv6PwWua?dl=0"
dbx = Dropbox(DROPBOX_TOKEN)


files = []

def handle_result(folder, folder_result):
    for item in folder_result.entries:
        if type(item) == FolderMetadata:
            get_files("/" + folder + "/" + item.name)
        else:
            files.append(folder + "/" + item.name)

def get_files(folder = ""):
    folder_result = dbx.files_list_folder(folder, shared_link = SharedLink(SHARED_LINK))
    handle_result(folder, folder_result)
    while folder_result.has_more:
        folder_result = dbx.files_list_folder_continue(folder_result.cursor)
        handle_result(folder, folder_result)

get_files()
print(f"Found {len(files)} files")

def get_shared_link(file):
    return dbx.sharing_get_shared_link_metadata(SHARED_LINK, file).url.replace("https://www", "https://dl") + "\n"

results = thread_map(get_shared_link, files)
with open("dropbox_links.txt", "a") as f:
    f.writelines(results)