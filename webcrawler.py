from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium.common.exceptions as err
from time import sleep


class Crawler():
    """
    wrapper around the selenium webdriver.
    """

    def __init__(self):
        self.driver = webdriver.Firefox()
        self.search_engine = 'https://duckduckgo.com'
        self.delay = 10  # seconds.

    def search(self, term, target):
        self.target = target
        self.driver.get(self.search_engine)
        try:
            search_bar = self.driver.find_element_by_id(
                'search_form_input_homepage')
            search_bar.send_keys(term)
            search_bar.send_keys(Keys.RETURN)

            elem_present = WebDriverWait(self.driver, self.delay).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'js-zci-link--images')))
            text = elem_present.text.lower()

            assert text.__contains__('images'), f'elem_present not located'

            imgBtn = self.driver.find_element_by_class_name(
                'js-zci-link--images')

            imgBtn.click()

            sleep(self.delay)

            crawled_enough = self.crawl()

            assert crawled_enough == True, "Not enough Images scrapped."

            yes = self.satisfied_with_images()

            assert yes == True, f'Not satisfied {yes}'

            self.download()

        except err.NoSuchElementException as e:
            print(e)
            self.driver.quit()
        except err.TimeoutException as e:
            print(e)
            self.driver.quit()
        except AssertionError as e:
            print(e)
            self.driver.quit()

    def satisfied_with_images(self):

        cmd = input(
            f'I have about {self.img_count()} images targeted \n will this be enough ? \n Enter (Y/N): ')
        if cmd.lower() == 'y':
            return True
        elif cmd.lower() == 'n':
            print('\t terminating WebCrawler.')
            self.driver.quit()
        else:
            return self.satisfied_with_images()

    def img_count(self):
        img_list = self.driver.find_elements_by_class_name('tile--img__img')
        # title_list = self.driver.find_elements_by_class_name('tile--img__title)
        return len(img_list)

    def crawl(self):

        if self.img_count() < self.target:
            print(':: ... searching for more images.')
            self.driver.execute_script(
                'window.scrollTo(0, document.body.scrollHeight);')
            return self.crawl()
        else:
            return True

    def download(self):
        print('\t ....downloading images....')
