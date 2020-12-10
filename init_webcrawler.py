from webcrawler import Crawler


def start():
    search_term = input(':: Enter search Term\n-> ')
    if len(search_term) > 0:
        try:
            max_n = int(input(':: Enter max number of image to scrape -> '))
            if max_n > 0:
                scrape(search_term, max_n)
                return
        except ValueError:
            start()

    start()


def scrape(term, max_n):
    print(':: .....Starting WebCrawler')
    driver = Crawler()
    driver.search(term, max_n)


start()
