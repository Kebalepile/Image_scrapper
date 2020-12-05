from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium.common.exceptions as err
from time import sleep


class WebCrawler:
    def __init__(self, webdriver):
        self.driver = webdriver.Firefox()
        self.url = "https://duckduckgo.com"
        self.delay = 10  # seconds
        self.target = 1

    def search(self, term, target):

        self.target = target

        try:
            self.driver.get(self.url)
            inputElem = self.driver.find_element_by_id(
                'search_form_input_homepage')
            inputElem.send_keys(term)
            inputElem.send_keys(Keys.RETURN)

            contains = WebDriverWait(self.driver, self.delay).until(
                EC.title_contains(term)
            )

            search_url = self.driver.current_url

            if contains:
                imgsBtn = WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="duckbar_static"]/li/a[contains(text(),"Images")]')))

                imgsBtn.click()

                sleep(self.delay)

                done_scrolling = self.scroll()

                assert done_scrolling == True, f' value is -> {done_scrolling}'

                self.botsa()

            else:
                print(f'title does not contain {term}')
                self.driver.quit()

        except err.NoSuchElementException:
            self.driver.quit()
            print('Did not find element you were looking for.')

        except err.TimeoutException:
            print('Loading took too much time')
            self.quit_driver()

    def img_count(self):
        imgs = self.driver.find_elements_by_css_selector(
            'img[class="tile--img__img  js-lazyload"]')

        return len(imgs)

        # titles = self.driver.find_elements_by_css_selector(
        #             'span[class="tile--img__title"]')
    def scroll(self):
        size = self.img_count()
        if size < self.target:
            print("\n....... searching for more images.")
            self.driver.execute_script(
                'window.scrollTo(0, document.body.scrollHeight)')
            sleep(3)
            return self.scroll()
        else:
            return True

    def botsa(self):
        cmd = input(
            f'\n I have about {self.img_count()} downloadable images \n\n please inspect what you see in the broswer \n\n and reply with (Y/N) to countiue or discard and quit.\n\n -> ::')
        if cmd.lower() == 'y':
            print("\n\t Scrape time !!!")
        elif cmd.lower() == 'n':
            print('....Bye')
            self.driver.quit()
        else:
            self.botsa()
