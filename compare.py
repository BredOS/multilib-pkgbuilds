import subprocess
import time
import urllib.request
import tarfile
from os import mkdir, listdir
from shutil import rmtree

import conf

def download_lists():
    foldern = 0
    for i in conf.repos:
        mkdir(str(foldern) + "-repo")
        stream = urllib.request.urlopen(i)
        with tarfile.open(fileobj=stream, mode="r|gz") as f:
            f.extractall(path=f"./{foldern}-repo/")
        print(f"Downloaded package list into ./{foldern}-repo/")
        foldern += 1

def clean():
    for i in listdir():
        if i.endswith("-repo"):
            print(f"Removing ./{i}/")
            rmtree(i)

def compare_lists():
    download_lists()
    clean()
