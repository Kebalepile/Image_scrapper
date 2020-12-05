from selenium import webdriver
from scrapper import WebCrawler

def search_term():
    term = input(':: Enter search term or sentence .i.e "King of the hill" \n:: --> ')
    if len(term) > 0:
        print(':: search in progress.')
        return term
    return search_term()

def start(n):
    crawl = WebCrawler(webdriver)
    crawl.search(search_term(), n)


def ask():
    num_of_downloads = int(
        input(':: Enter maximum number of images to download: \n'))
    if num_of_downloads <= 0:
        ask()
    else:
        print(" \n.........starting WebCrawler.")
        start(num_of_downloads)


ask()
