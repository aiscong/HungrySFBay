from selenium import webdriver
import time
import requests
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from urllib.parse import urlparse


class Util:
    delay = 10  # seconds

    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-infobars")
        self.driver = webdriver.Chrome(executable_path='./chromedriver', chrome_options=chrome_options)

    def log_in(self, username, password):
        self.driver.get("https://www.instagram.com/accounts/login")
        try:
            user_name_form = WebDriverWait(self.driver, self.delay).until(
                EC.presence_of_element_located((By.NAME, "username")))
            user_name_form.send_keys(username)

            password_form = WebDriverWait(self.driver, self.delay).until(
                EC.presence_of_element_located((By.NAME, "password")))
            password_form.send_keys(password)

            log_in_button = WebDriverWait(self.driver, self.delay).until(
                EC.presence_of_element_located((By.XPATH, "//button[@type='submit']")))
            log_in_button.click()

            not_now_popup = WebDriverWait(self.driver, self.delay).until(
                EC.presence_of_element_located((By.XPATH, "//button[contains(text(),'Not Now')]")))
            not_now_popup.click()
        except TimeoutException:
            print("Loading took too much time!")

    def search_by_tag(self, tag):
        self.driver.get("https://www.instagram.com/explore/tags/" + tag)

    def get_tagged_page_urls_from_post_url(self, post_url):
        self.driver.get(post_url)
        page_url_set = set()
        for tagged_page in self.driver.find_elements_by_xpath("//a[@class='JYWcJ']"):
            page_url_set.add(tagged_page.get_attribute("href"))
        print(page_url_set)
        return page_url_set

    def get_post_urls_by_tag(self, tag):
        post_url_set = set()
        self.search_by_tag(tag)
        try:
            thumbnail_list = WebDriverWait(self.driver, self.delay).until(
                EC.presence_of_all_elements_located((By.XPATH, "//div[@class='eLAPa']/parent::a")))
            for thumbnail in thumbnail_list:
                post_url_set.add(thumbnail.get_attribute("href"))
        except TimeoutException:
            print("Loading took too much time!")

        print(post_url_set, sep="\n")
        return post_url_set
        # thumbnail_href = thumbnail_list[0].get_attribute("href")
        # self.driver.get(thumbnail_href)
        # time.sleep(1)
        # photo_url = self.driver.find_element_by_xpath("//img[@class='FFVAD']").get_attribute("src")
        # self.driver.get(photo_url)
        # requests.get(photo_url).content
        # with open('image_name.jpg', 'wb') as handler:
        #     handler.write(img_data)
        #
        # print(len(thumbnail_list))

    def build_page_from_page_url(self, page_url):
        self.driver.get(page_url)

        try:
            follower_element = WebDriverWait(self.driver, self.delay).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//a[@href='{}followers/']/span".format(urlparse(page_url).path))))
            following_element = WebDriverWait(self.driver, self.delay).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//a[@href='{}following/']/span".format(urlparse(page_url).path))))
            num_post_elment = WebDriverWait(self.driver, self.delay).until(
                EC.presence_of_element_located((By.XPATH,
                                                "//a[@href='{}followers/']/span/ancestor::ul/li[1]/span/span".format(
                                                    urlparse(page_url).path))))
            nick_name_element = WebDriverWait(self.driver, self.delay).until(
                EC.presence_of_element_located((By.XPATH, "//h1[@class='rhpdm']")))

            try:
                bio_link = self.driver.find_element_by_xpath("//h1[@class='rhpdm']/parent::div/a")
                # print("https://{}".format(bio_link.text))
            except NoSuchElementException:
                pass

            print(self.driver.find_element_by_xpath("//h1[@class='rhpdm']/parent::div/span").text)

        except TimeoutException:
            print("Loading took too much time!")
        # self.driver.find_element_by_xpath(
        #     "//a[@href='{}followers/']/span".format(urlparse(page_url).path)).get_attribute("title")
        return
