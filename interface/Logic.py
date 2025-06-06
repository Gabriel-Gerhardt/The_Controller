import os
from pathlib import Path


def getPath():
    return os.getcwd();


def getChildren(path):
    return os.listdir(path);

def main():
    print(getPath());
    print(getChildren(getPath()));

main()
